import httpx
from fastapi import HTTPException
from ..config import ACCOUNT_BASE_URL, HTTP_TIMEOUT_SECONDS
from ..utils import normalize_iban

global_client = httpx.Client(timeout = HTTP_TIMEOUT_SECONDS)

def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

def close_client() -> None:
    global_client.close()

def assert_owns_account(from_account_id: str, token: str) -> None:
    url = f"{ACCOUNT_BASE_URL}/accounts/{from_account_id}"
    
    try:
        res = global_client.get(url, headers = auth_header(token))
    except httpx.RequestError as e:
        raise HTTPException(status_code = 502, detail=f"Account service is unreachable: {e}")
    
    if res.status_code == 200:
        return
    if res.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if res.status_code == 403:
        raise HTTPException(status_code=403, detail="Forbidden: from_account_id is not yours")
    if res.status_code == 404:
        raise HTTPException(status_code=404, detail="Recipient IBAN not found")

    raise HTTPException(status_code=502, detail=f"Account service error: {res.status_code} {res.text}")
    
def lookup_recipient_by_iban(to_iban: str, token: str) -> dict:
    iban_normal = normalize_iban(to_iban)
    url = f"{ACCOUNT_BASE_URL}/accounts/by-iban/{iban_normal}"

    try:
        res = global_client.get(url, headers = auth_header(token))
    except httpx.RequestError as e:
        raise HTTPException(status_code = 502, detail=f"Account service is unreachable: {e}")

    if res.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if res.status_code == 404:
        raise HTTPException(status_code=404, detail="from_account_id not found")
    if res.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"Account service error: {res.status_code} {res.text}")
    
    return res.json()