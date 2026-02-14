from fastapi import Header, HTTPException
from jose import jwt, JWTError
from .config import JWT_SECRET, JWT_ALG

def get_curr_user(authorization: str = Header(default="")) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization")
    
    token = authorization.split(" ", 1)[1].strip() #Što se ovjde dogada s obzirom da se prvi put pojavljuje u projektu

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing sub")
    
    return {"user_id": user_id, "claims": payload, "token": token}