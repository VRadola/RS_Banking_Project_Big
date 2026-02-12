from fastapi import FastAPI
from .routers.transactions import router as transaction_router
from contextlib import asynccontextmanager
from .clients.account_client import close_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_client()

app = FastAPI(title="Transaction Service", lifespan=lifespan)
app.include_router(transaction_router)

@app.get("/health")
def health():
    return {"status": "ok"}