import httpx
from fastapi import HTTPException
from ..config import ACCOUNT_BASE_URL, HTTP_TIMEOUT_SECONDS
from ..utils import normalize_iban

def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

def assert_owns_account(from_account_id: str, token: str) -> None:
    url = f"{ACCOUNT_BASE_URL}/accounts/{from_account_id}"
    with httpx.Client(timeout=HTTP_TIMEOUT_SECONDS) as client:
        result = client.get(url, headers=auth_header(token))

    if result.status_code == 401:
        raise HTTPException(status_code = 401, detail="Unauthorized")
    if result.status_code == 403:
        raise HTTPException(status_code= 403, detail="This is not your account")
    if result.status_code == 404:
        raise HTTPException(status_code = 404, detail="Account not found")
    if result.status_code >= 400:
        raise HTTPException(status_code = 502, detail=f"Account service error: {result.status_code} {result.text}")
    
def lookup_recipient_by_iban(to_iban: str, token: str) -> dict:
    iban_normal = normalize_iban(to_iban)
    url = f"{ACCOUNT_BASE_URL}/accounts/by-iban/{iban_normal}"

    with httpx.Client(timeout=HTTP_TIMEOUT_SECONDS) as client:
        result = client.get(url, headers=auth_header(token))
    
    if result.status_code == 404:
        raise HTTPException(status_code = 404, detail="Recipient IBAN not found")
    if result.status_code == 401:
        raise HTTPException(status_code = 401, detail="Unauthorized")
    if result.status_code >= 400:
        raise HTTPException(status_code = 502, detail=f"Account service error: {result.status_code} {result.text}")
    
    return result.json()