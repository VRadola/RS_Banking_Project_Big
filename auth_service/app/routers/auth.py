from fastapi import APIRouter
from ..schemas import RegisterIn, LoginIn, TokenOut
from ..services.auth_logic import register_user, login_user

router = APIRouter()

@router.post("/register")
def register(body: RegisterIn):
    return register_user(body.username, body.password)

@router.post("/login")
def login(body: LoginIn):
    return login_user(body.username, body.password)