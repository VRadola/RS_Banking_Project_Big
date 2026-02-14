import uuid
from datetime import datetime, timezone, timedelta
from jose import jwt
from .config import JWT_SECRET, JWT_ALG, JWT_EXPIRES_MIN

def iso_utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def new_user_id():
    return f"USR_{uuid.uuid4()}"

def create_token(user_id: str):
    exp = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRES_MIN)
    token = {
        "sub": user_id,
        "exp": exp,
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(token, JWT_SECRET, algorithm=JWT_ALG)