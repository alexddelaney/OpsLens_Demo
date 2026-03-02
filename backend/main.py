"""
OpsLens Backend Entry Point

What this file does:
- Loads environment variables
- Creates FastAPI app
- Provides health check
- Prepares for router expansion
"""

# =========================
# 1. Load environment vars
# =========================
from app.core.scheduler import start_scheduler
from dotenv import load_dotenv
import os

# Loads variables from .env into process environment
load_dotenv()

# Pull database URL (used later by SQLAlchemy)
DATABASE_URL = os.getenv("DATABASE_URL")

# Optional safety check (helps debugging)
if not DATABASE_URL:
    print("WARNING: DATABASE_URL is not set")


# =========================
# 2. Create FastAPI app
# =========================

from fastapi import FastAPI

app = FastAPI(
    title="OpsLens API",
    description="Operational intelligence and monitoring platform",
    version="0.1.0",
)

@app.on_event("startup")
def start_background_jobs():
    start_scheduler()
    
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ← IMPORTANT
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 3. Health check endpoint
# =========================

@app.get("/health")
def health_check():
    """
    Simple endpoint to verify backend is alive.

    Used by:
    - browser tests
    - load balancers
    - uptime monitors
    """
    return {"status": "ok"}

# =========================
# Create database tables (DEV ONLY)
# =========================

from app.db.session import engine
from app.models.metric import Metric

# Automatically create tables in development
Metric.metadata.create_all(bind=engine)



# =========================
# 4. from app.api import routes
# app.include_router(routes.router)
# =========================
# Register API routers
# =========================

from app.api.metrics import router as metrics_router

app.include_router(metrics_router)
