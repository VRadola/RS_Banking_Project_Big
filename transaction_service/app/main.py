from fastapi import FastAPI
from .routers.transactions import router as transaction_router
from contextlib import asynccontextmanager
from .clients.account_client import close_client
from fastapi.middleware.cors import CORSMiddleware
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_client()

app = FastAPI(title="Transaction Service", lifespan=lifespan)
app.include_router(transaction_router)

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