from fastapi import HTTPException
from ..database.db import ddb_client
from ..config import DDB_PAYMENTS_TABLE, IDEMP_TTL_SECONDS
from ..utils import iso_utc_now, new_payment_id, new_epoch, normalize_iban, normalize_name
from ..clients.account_client import assert_owns_account, lookup_recipient_by_iban
from ..clients.transaction_client import transaction_transfer

def pk_acc(account_id: str) -> str:
    return account_id if account_id.startswith("ACC#") else f"ACC#{account_id}"

def create_payment(user_id: str, token: str, from_account_id: str, to_iban: str, payee_name: str,
                   amount_cents: int, idempotency_key: str, reference: str | None):
    assert_owns_account(from_account_id, token)

    recipient = lookup_recipient_by_iban(to_iban, token)
    to_account_id = recipient.get("account_id")
    official_name = recipient.get("owner_name", "")

    if not to_account_id:
        raise HTTPException(status_code = 502, detail="User not found!")
    
    if normalize_name(payee_name) != normalize_name(official_name):
        raise HTTPException(status_code = 400, detail="Name is not valid! Please enter correct name.")
    
    now = iso_utc_now()
    payment_id = new_payment_id()
    ttl = new_epoch() + IDEMP_TTL_SECONDS

    idemp_pk = f"IDEMP#{idempotency_key}"
    pay_pk = pk_acc(from_account_id)
    pay_sk = f"{now}#PAY#{payment_id}"
    to_iban_norm = normalize_iban(to_iban)

    try:
        ddb_client.transact_write_items(
            TransactItems = [
                {
                    "Put": {
                        "TableName": DDB_PAYMENTS_TABLE,
                        "Item": {
                            "PK": {"S": idemp_pk},
                            "SK": {"S": "PAY"},
                            "payment_id": {"S": payment_id},
                            "ttl": {"N": str(ttl)}
                        },
                        "ConditionExpression": "attribute_not_exists(PK)"
                    }
                },
                {
                    "Put": {
                        "TableName": DDB_PAYMENTS_TABLE,
                        "Item": {
                            "PK": {"S": pay_pk},
                            "SK": {"S": pay_sk},
                            "payment_id": {"S": payment_id},
                            "user_id": {"S": user_id},
                            "from_account_id": {"S": from_account_id},
                            "to_iban": {"S": to_iban_norm},
                            "to_account_id": {"S": to_account_id},
                            "payee_name": {"S": official_name},
                            "amount_cents": {"N": str(amount_cents)},
                            "status": {"S": "INITIATED"},
                            "idempotency_key": {"S": idempotency_key},
                            "created_at": {"S": now},
                            **({"reference": {"S": reference}} if reference else {} )
                        }
                    }
                }
            ]
        )
    except ddb_client.exceptions.TransactionCanceledException:
        raise HTTPException(status_code = 409, detail="Duplicate payment")
    
    try:
        trans_res = transaction_transfer(from_account_id, to_account_id, amount_cents, idempotency_key, token)
        transaction_tx_id = trans_res.get("tx_id") or trans_res.get("transaction_id")
    except HTTPException as e:
        update_status(pay_pk, pay_sk, "FAILED", None)
        raise e
    
    update_status(pay_pk, pay_sk, "COMPLETED", transaction_tx_id)

    return {"payment_id": payment_id, "status": "COMPLETED", "transaction_tx_id": transaction_tx_id}

def update_status(pk: str, sk: str, status: str, transaction_tx_id: str | None):
    expr = "SET #s=:s, updated_at=:u"
    names = {"#s": "status"}
    values = {
        ":s": {"S": status},
        ":u": {"S": iso_utc_now()}
    }

    if transaction_tx_id:
        expr += ", transaction_tx_id=:t"
        values[":t"] = {"S": transaction_tx_id}

    ddb_client.update_item(
        TableName = DDB_PAYMENTS_TABLE,
        Key = {"PK": {"S": pk}, "SK": {"S": sk}},
        UpdateExpression = expr,
        ExpressionAttributeNames = names,
        ExpressionAttributeValues = values
    )