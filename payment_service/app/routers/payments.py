from fastapi import APIRouter, Depends
from ..auth import get_curr_user
from ..schemas import CreatePaymentIn
from ..services.payments import create_payment

router = APIRouter()

@router.post("/")
def make_payment(body: CreatePaymentIn, user = Depends(get_curr_user)):
    return create_payment(
        user_id = user["user_id"],
        token = user["token"],
        from_account_id = body.from_account_id,
        to_iban = body.to_iban,
        payee_name = body.payee_name,
        amount_cents = body.amount_cents,
        idempotency_key = body.idempotency_key,
        reference = body.reference
    )