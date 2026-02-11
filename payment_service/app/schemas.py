from pydantic import BaseModel, Field
from typing import Optional

class CreatePaymentIn(BaseModel):
    from_account_id: str
    to_iban: str
    payee_name: str
    amount_cents: int = Field(gt=0)
    idempotency_key: str = Field(min_length=8, max_length=128)
    reference: Optional[str] = None

class PaymentOut(BaseModel):
    payment_id: str
    status: str
    ledger_tx_id: str | None = None