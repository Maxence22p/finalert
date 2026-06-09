from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.routes import transactions, alerts

app = FastAPI(
    title="FinAlert API",
    description="Système de monitoring de transactions financières",
    version="1.0.0"
)

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Routes
app.include_router(transactions.router)
app.include_router(alerts.router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"app": "FinAlert", "version": "1.0.0"}