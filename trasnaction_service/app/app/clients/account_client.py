import httpx
from fastapi import HTTPException
from ..config import ACCOUNT_BASE_URL, HTTP_TIMEOUT_SECONDS

global_client = httpx.Client(timeout = HTTP_TIMEOUT_SECONDS)

def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

def close_client() -> None:
    global_client.close()

def assert_owns_account(account_id: str, token: str) -> None:
    url = f"{ACCOUNT_BASE_URL}/accounts/{account_id}"
    
    try:
        res = global_client.get(url, headers = auth_header(token))
    except httpx.RequestError as e:
        raise HTTPException(status_code = 502, detail=f"Account service is unreachable: {e}")

    if res.status_code == 200:
        return
    if res.status_code == 401:
        raise HTTPException(status_code = 401, detail="Unauthorized")
    if res.status_code == 403:
        raise HTTPException(status_code= 403, detail="This is not your account")
    if res.status_code == 404:
        raise HTTPException(status_code = 404, detail="Account not found")
    
    raise HTTPException(status_code = 502, detail=f"Account service error: {res.status_code} {res.text}")