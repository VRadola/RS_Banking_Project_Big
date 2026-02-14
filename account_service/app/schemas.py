from pydantic import BaseModel, Field
from typing import Optional, List

class AccountCreateIn(BaseModel):
    name: Optional[str] = Field(default="Main")

class AccountOut(BaseModel):
    account_id: str
    user_id: str
    iban: str
    status: str
    name: str
    created_at: str

class CardOut(BaseModel):
    card_id: str
    account_id: str
    user_id: str
    brand: str
    pan_masked: str
    last4: str
    exp_month: int
    exp_year: int
    status: str
    created_at: str

class AccountCreateOut(BaseModel):
    account: AccountOut
    card: CardOut