import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")

DDB_ACCOUNTS_TABLE = os.getenv("DDB_ACCOUNTS_TABLE", "Account_Service_table")
DDB_CARDS_TABLE = os.getenv("DDB_CARDS_TABLE", "Card_Service_table")

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is missing in .env")
