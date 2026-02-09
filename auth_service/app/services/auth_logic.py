from fastapi import HTTPException
from passlib.context import CryptContext
from boto3.dynamodb.conditions import Key
from ..database.db import users_table
from ..utils import new_user_id, iso_utc_now, create_token
from ..config import JWT_EXPIRES_MIN

passwd = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def register_user(username: str, raw_password: str):
    username = username.strip().lower()

    username_exists = users_table.query(
        IndexName = "username-index",
        KeyConditionExpression = Key("username").eq(username),
        Limit = 1 
    )

    if username_exists.get("Items"):
        raise HTTPException(status_code=409, detail="Username already exists")
    
    user_id = new_user_id()
    password_hash = passwd.hash(raw_password)

    users_table.put_item(
        Item = {
            "user_id": user_id,
            "username": username,
            "password_hash": password_hash,
            "created_at": iso_utc_now()
        },
        ConditionExpression = "attribute_not_exists(user_id)"
    )

    token = create_token(user_id)

    return {
        "access_token": token,
        "expires_in": JWT_EXPIRES_MIN * 60,
        "user_id": user_id    
    }

def login_user(username: str, raw_password: str):
    username = username.strip().lower()

    result = users_table.query(
        IndexName = "username-index",
        KeyConditionExpression = Key("username").eq(username),
        Limit = 1
    )

    items = result.get("Items", [])
    if not items:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = items[0]

    if not passwd.verify(raw_password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user["user_id"])

    return {
        "access_token": token,
        "expires_in": JWT_EXPIRES_MIN * 60,
        "user_id": user["user_id"]
    }