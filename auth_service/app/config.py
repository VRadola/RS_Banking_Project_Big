import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
DDB_USERS_TABLE = os.getenv("DDB_USERS_TABLE", "Users_Service_table")

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "60"))

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is missing")