import httpx
from fastapi import HTTPException
from ..config import TRANSACTION_BASE_URL, HTTP_TIMEOUT_SECONDS

global_client = httpx.Client(timeout = HTTP_TIMEOUT_SECONDS)

def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

def close_client() -> None:
    global_client.close()

def transaction_transfer(from_account_id: str, to_account_id: str, amount_cents: int, idempotency_key: str, token: str) -> dict:
    url = f"{TRANSACTION_BASE_URL}/transactions/payment"
    body = {
        "from_account_id": from_account_id,
        "to_account_id": to_account_id,
        "amount_cents": amount_cents,
        "idempotency_key": idempotency_key
    }

    try:
        res = global_client.post(url, json = body, headers = auth_header(token))
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Transaction service is unreachable: {e}")

    if res.status_code == 409:
        raise HTTPException(status_code=409, detail="Insufficient funds or duplicate request")
    if res.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if res.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"Transaction service error: {res.status_code} {res.text}")
    
    return res.json()