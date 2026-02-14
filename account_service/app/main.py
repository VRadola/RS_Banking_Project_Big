from fastapi import FastAPI
from .routers.accounts import router as accounts_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Account Service")
app.include_router(accounts_router)

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