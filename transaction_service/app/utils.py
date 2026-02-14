from datetime import datetime, timezone
import uuid
import time

def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")

def new_transaction_id() -> str:
    return f"TX_{uuid.uuid4()}"

def now_epoch() -> int:
    return int(time.time())

def ensure_acc_pk(account_id: str) -> str:
    return account_id if account_id.startswith("ACC#") else f"ACC#{account_id}"

def idem_pk(idempotency_key: str) -> str:
    return f"IDEMP#{idempotency_key}"