import uuid, time
from datetime import datetime, timezone

def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")

def new_payment_id() -> str:
    return f"PAY#{uuid.uuid4()}"

def new_epoch() -> int:
    return int(time.time())

def normalize_iban(iban: str) -> str:
    return iban.strip().upper().replace(" ", "")

def normalize_name(name: str) -> str:
    return " ".join(name.strip().upper().split())