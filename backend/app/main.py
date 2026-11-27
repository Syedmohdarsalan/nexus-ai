"""FastAPI entry point. Run migrations before starting the server."""
from fastapi import FastAPI
from .invoices import router

app = FastAPI(
    title="NEXUS AI",
    description="Local development API for simulated financial operations. No real funds.",
    version="0.1.0",
)
app.include_router(router)

@app.get("/", tags=["System"])
def home():
    return {"project": "NEXUS AI", "status": "running", "phase": "1.1"}

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}
