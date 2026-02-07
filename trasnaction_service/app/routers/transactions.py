from fastapi import APIRouter, Depends, HTTPException
from boto3.dynamodb.conditions import Key
from auth import get_curr_user
from database.db import transaction_table
from schemas import DepositIn, TransferIn, TransactionOut, BalanceOut
from services.transaction import deposit_atomic, transfer_atomic
from utils import ensure_acc_pk

router = APIRouter()

@router.get("/transactions/balance/{accound_id}")
def get_balance(account_id: str, user=Depends(get_curr_user)):
    pk = ensure_acc_pk(account_id)
    resp = transaction_table.get_item(Key = {"PK": pk, "SK": "BALANCE"})
    item = resp.get("Item") or {}
    available = int(item.get("available_cents", 0))
    
    return {"accound_id": account_id, "available_cents": available}

@router.post("/transactions/deposit")
def deposit(body: DepositIn, user=Depends(get_curr_user)):
    return deposit_atomic(body.accound_id, body.amount_cents, body.idempotency_key)

@router.post("/transactions/transfer")
def transfer(body: TransferIn, user=Depends(get_curr_user)):
    return transfer_atomic(body.from_account_id, body.to_account_id, body.amount_cents, body.idempotency_key)

@router.get("/transactions/history/{account_id}")
def history(account_id: str, user=Depends(get_curr_user), limit: int = 50):
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 200")
    pk = ensure_acc_pk(account_id)

    resp = transaction_table.query(
        KeyConditionExpression = Key("PK").eq(pk) & Key("SK").begins_with("20"),
        Limit = limit,
        ScanIndexForward = False
    )
    return resp.get("Items", [])