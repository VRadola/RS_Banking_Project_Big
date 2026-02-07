from fastapi import FastAPI
from routers.transactions import router as transaction_router

app = FastAPI(title="Transaction Service")
app.include_router(transaction_router)

app.get("/health")
def health():
    return {"status": "ok"}