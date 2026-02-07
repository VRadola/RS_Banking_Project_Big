from fastapi import Header, HTTPException
from jose import jwt, JWTError
from config import JWT_ALG, JWT_SECRET

def get_curr_user(auth: str = Header(default="")) -> dict:
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing | Invalid authorization header")
    
    token = auth.removeprefix("Bearer ").strip()
    try:
        decode = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = decode.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing sub")
    
    return {
        "user_id": user_id, 
        "claims": decode
    }