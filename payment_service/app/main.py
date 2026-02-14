from fastapi import FastAPI
from .routers.payments import router as payments_router
from contextlib import asynccontextmanager
from .clients.account_client import close_client as cc_acc
from .clients.transaction_client import close_client as cc_trans
from fastapi.middleware.cors import CORSMiddleware
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    cc_acc()
    cc_trans()

app = FastAPI(title="Payment Service", lifespan=lifespan)
app.include_router(payments_router)

"""app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)"""

@app.get("/health")
def health():
    return {"status": "ok"}