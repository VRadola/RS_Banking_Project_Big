from fastapi import FastAPI
from routers.accounts import router as accounts_router

app = FastAPI(title="Account Service")
app.include_router(accounts_router)

@app.get("/health")
def health():
    return {"status": "ok"}