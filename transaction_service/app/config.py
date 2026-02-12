import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
DDB_TRANSACTION_TABLE = os.getenv("DDB_TRANSACTION_TABLE", "Transaction_Service_table")

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

IDEMP_TTL_SECONDS = int(os.getenv("IDEMP_TTL_SECONDS", "86400"))

ACCOUNT_BASE_URL = os.getenv("ACCOUNT_BASE_URL", "http://127.0.0.1:8001")
HTTP_TIMEOUT_SECONDS = float(os.getenv("HTTP_TIMEOUT_SECONDS", "10"))

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is missing in .env")