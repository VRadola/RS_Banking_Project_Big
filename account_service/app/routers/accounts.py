from fastapi import APIRouter, Depends, HTTPException
from boto3.dynamodb.conditions import Key
from app import auth
from database.db import cards_table, accounts_table, db_client
from schemas import AccountCreateIn, AccountCreateOut, CardOut, AccountOut
from utils import iso_utc_now, new_account_id, new_card_id, generate_iban, generate_pan, mask_pan
from decimal import Decimal

router = APIRouter()

router.post("/accounts")
def create_account(body: dict, user = Depends(auth.get_curr_user)):
    user_id = user["user_id"]
    now = iso_utc_now()
    account_id = new_account_id()
    iban = generate_iban()
    card_id = new_card_id()
    brand = "VISA"
    pan = generate_pan(brand=brand)
    pan_masked, last4 = mask_pan(pan)
    exp_month = 12
    exp_year = 2029

    accounts_item = {
       "account_id": account_id,
       "user_id": user_id,
       "iban": iban,
       "status": "ACTIVE",
       "name": body.name or "Main",
       "created_at": now
    }

    cards_item = {
        "card_id": card_id,
        "account_id": account_id,
        "user_id": user_id,
        "brand": brand,
        "pan": pan,
        "pan_masked": pan_masked,
        "last4": last4,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "status": "ACTIVE",
        "created_at": now
    }

    try:
        db_client.transact_write_items(
            TransactItems = [
                {
                    "Put": {
                        "TableName": accounts_table.name,
                        "Item": {k: {"S": str(v)} for k, v in accounts_item.items()},
                        "ConditionExpression": "attribute_not_exists(account_id)"
                    }
                },
                {
                    "Put": {
                        "TableName": cards_table.name,
                        "Item": {k: {"S": str(v)} for k, v in cards_item.items()}, #Sto se radi ovdje u viticastim zagradama
                        "ConditionExpression": "attribute_not_exists(card_id)"
                    }
                }
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create account/card: {e}")
    
    return {
        "account": accounts_item,
        "card": {**{k: v for k, v in cards_item.items() if k != "pan"}} # sto predstavljaju ** te zasto pan u ""
    }

@router.get("/accounts")
def list_accounts(user = Depends(auth.get_curr_user)):
    user_id = user["user_id"]
    resp = accounts_table.query(
        IndexName = "user_id-index",
        KeyConditionExpression = Key("user_id").eq(user_id),
        ScanIndexForward = False
    )
    return resp.get("Items", [])

@router.get("/accounts/{account_id}")
def get_account(accound_id: str, user = Depends(auth.get_curr_user)):
    user_id = user["user_id"]
    resp = accounts_table.get_item(Key = {"account_id": accound_id})
    item = resp.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Account not found")
    if item.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access not allowed")
    return item

@router.get("/accounts/{account_id}/cards")
def list_cards_for_acc(account_id: str, user = Depends(auth.get_curr_user)):
    user_id = user["user_id"]
    acc = accounts_table.get_item(Key = {"account_id": account_id}).get("Item")
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    if acc.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access not allowed")
    
    resp = cards_table.query(
        IndexName = "account_id-index" ,
        KeyConditionExpression = Key("accound_id").eq(account_id),
        ScanIndexForward = False
    )
    items = resp.get("Items", [])

    for it in items:
        it.pop("pan", None)
    
    return items