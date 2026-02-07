from fastapi import HTTPException
from database.db import db_client
from config import DDB_TRANSACTION_TABLE, IDEMP_TTL_SECONDS
from utils import iso_utc_now, new_transaction_id, now_epoch, ensure_acc_pk, idem_pk

def get_balance_item(account_id: str) -> dict:
    raise NotImplementedError

def deposit_atomic(account_id: str, amount_cents: int, idempotency_key: str) -> dict:
    now = iso_utc_now()
    transaction_id = new_transaction_id()
    pk = ensure_acc_pk(account_id)
    idem = idem_pk(idempotency_key)
    ttl = now_epoch() + IDEMP_TTL_SECONDS #sto je idempotency u ovom projektu zasto je bitan te sto predstavlja ttl

    try:
        db_client.transact_write_items(
            TransactItems = [
                {
                    "Put": {
                        "TableName": DDB_TRANSACTION_TABLE,
                        "Item": {
                            "PK": {"S": idem},
                            "SK": {"S": "Transaction"},
                            "transaction_id": {"S": transaction_id},
                            "ttl": {"N": str(ttl)}
                        },
                        "ConditionExpression": "attribute_not_exists(PK)"
                    }
                },

                {
                    "Update": {
                        "TableName": DDB_TRANSACTION_TABLE,
                        "Key": {"PK": {"S": pk}, "SK": {"S": "BALANCE"}},
                        "UpdateExpression": "SET available_cents = if not_exists(available_cents, :zero) + :amount, updated_at=:now",
                        "ExpressionAttributeValues": {
                            ":amount": {"N": str(amount_cents)},
                            ":zero": {"N": "0"},
                            ":now": {"S": now}
                        }
                    }
                },

                {
                    "Put": {
                        "TableName": DDB_TRANSACTION_TABLE,
                        "Item": {
                            "PK": {"S": pk},
                            "SK": {"S": f"{now}#TX#{transaction_id}"},
                            "transaction_id": {"S": transaction_id},
                            "type": {"S": "DEPOSIT"},
                            "amount_cents": {"N": str(amount_cents)},
                            "status": {"S": "COMMITTED"},
                            "idempotency_key": {"S": idempotency_key},
                            "created_at": {"S": now}
                        }
                    }
                }
            ]
        )
    except db_client.exceptions.TransactionCanceledException:
        raise HTTPException(status_code=409, detail="Duplicate request or transaction canceled")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deposit failed: {e}")
    
    return {"transaction_id": transaction_id, "status": "COMMITTED"}

def transfer_atomic(from_account_id: str, to_account_id: str, amount_cents: int, idempotency_key: str) -> dict:
    if from_account_id == to_account_id:
        raise HTTPException(status_code=400, detail="Trying to transfer money to yourself")
    
    now = iso_utc_now()
    transaction_id = new_transaction_id()
    from_pk = ensure_acc_pk(from_account_id)
    to_pk = ensure_acc_pk(to_account_id)
    idem = idem_pk(idempotency_key)
    ttl = now_epoch() + IDEMP_TTL_SECONDS

    try:
        db_client.transact_write_items(
            TransactItems = [
                {
                    "Put": {
                        "TableName": DDB_TRANSACTION_TABLE,
                        "Item": {
                            "PK": {"S": idem},
                            "SK": {"S": "Transaction"},
                            "transaction_id": {"S": transaction_id},
                            "ttl": {"N": str(ttl)}
                        },
                        "ConditionExpression": "attribute_not_exists(PK)"
                    }
                },

                {
                    "Update": {
                        "TableName": DDB_TRANSACTION_TABLE,
                        "Key": {"PK": {"S": from_pk}, "SK": {"S": "BALANCE"}},
                        "UpdateExpression": "SET available_cents = if_not_exists(available_cents, :zero) - :amount, updated_at=:now",
                        "ConditionExpression": "if_not_exists(available_cents, :zero) >= :amount",
                        "ExpressionAttributeValues": {
                            ":amount": {"N": str(amount_cents)},
                            ":zero": {"N": "0"},
                            ":now": {"S": now}
                        }
                    }
                },

                {
                    "Update": {
                        "TableName": DDB_TRANSACTION_TABLE,
                        "Key": {"PK": {"S": to_pk}, "SK": {"S": "BALANCE"}},
                        "UpdateExpression": "SET available_cents = if_not_exists(available_cents, :zero) + :amount, updated_at=:now",
                        "ExpressionAttributeValues": {
                            ":amount": {"N": str(amount_cents)},
                            ":zero": {"N": "0"},
                            ":now": {"S": now}
                        }
                    }
                },

                {
                    "Put": {
                        "TableName": DDB_TRANSACTION_TABLE,
                        "Item": {
                            "PK": {"S": to_pk},
                            "SK": {"S": f"{now}#TX#{transaction_id}#OUT"},
                            "transaction_id": {"S": transaction_id},
                            "type": {"S": "TRANSFER_OUT"},
                            "amount_cents": {"N": str(-amount_cents)},
                            "counterparty_account_id": {"S": to_account_id},
                            "status": {"S": "COMMITTED"},
                            "idempotency_key": {"S": idempotency_key},
                            "created_at": {"S": now}
                        }
                    }
                },

                {
                    "Put": {
                        "TableName": DDB_TRANSACTION_TABLE,
                        "Item": {
                            "PK": {"S": to_pk},
                            "SK": {"S": f"{now}#TX#{transaction_id}#IN"},
                            "transaction_id": {"S": transaction_id},
                            "type": {"S": "TRANSFER_IN"},
                            "amount_cents": {"N": str(amount_cents)},
                            "counterparty_account_id": {"S": from_account_id},
                            "status": {"S": "COMMITTED"},
                            "idempotency_key": {"S": idempotency_key},
                            "created_at": {"S": now}
                        }
                    }
                }
            ]
        )
    except db_client.exceptions.TransactionCanceledException:
        raise HTTPException(status_code=409, detail="Insufficient funds or duplicate request")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transfer failed: {e}")
    
    return {"transaction_id": transaction_id, "status": "COMMITTED"}