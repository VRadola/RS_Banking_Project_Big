from fastapi import FastAPI
from .routers.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Auth_Service")
app.include_router(auth_router)

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