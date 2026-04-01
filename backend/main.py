"""
OpsLens Backend Entry Point
"""

# =========================
# 1. Load environment vars
# =========================
from app.api.routes.auth import router as auth_router
from app.api.metrics import router as metrics_router
from app.models.metric import Metric
from app.db.session import engine
from app.core.scheduler import start_scheduler
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("WARNING: DATABASE_URL is not set")

# =========================
# 2. Create FastAPI app
# =========================

app = FastAPI(
    title="OpsLens API",
    description="Operational intelligence and monitoring platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 3. Startup event
# =========================


@app.on_event("startup")
def start_background_jobs():
    start_scheduler()

# =========================
# 4. Health check
# =========================


@app.get("/health")
def health_check():
    return {"status": "ok"}


# =========================
# 5. Create database tables (DEV ONLY)
# =========================

Metric.metadata.create_all(bind=engine)

# =========================
# 6. Register routers
# =========================

app.include_router(metrics_router)
app.include_router(auth_router)
