from pydantic import BaseModel, Field

class DepositIn(BaseModel):
    account_id: str
    amount_cents: int = Field(gt=0)
    idempotency_key: str = Field(min_length=8, max_length=128)

class TransferIn(BaseModel):
    from_account_id: str
    to_account_id: str
    amount_cents: int = Field(gt=0)
    idempotency_key: str = Field(min_length=8, max_length=128)

class TransactionOut(BaseModel):
    transaction_id: str
    status: str

class BalanceOut(BaseModel):
    account_id: str
    available_cents: int