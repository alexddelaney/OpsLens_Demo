"""
Metrics API routes.

Provides:
- POST /metrics → ingest data
- GET /metrics → list data (protected)
- POST /metrics/collect → manual collection
- GET /metrics/alerts → anomaly detection (protected)
"""

from fastapi import WebSocket, WebSocketDisconnect
import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.metric import Metric
from app.models.user import User
from app.schemas.metric import MetricCreate, MetricResponse
from app.core.analytics import detect_spike
from app.core.collector import collect_system_metrics
from app.core.security import get_current_user

router = APIRouter(prefix="/metrics", tags=["metrics"])


# CREATE METRIC

@router.post("/", response_model=MetricResponse)
def create_metric(metric: MetricCreate, db: Session = Depends(get_db)):
    db_metric = Metric(
        name=metric.name,
        value=metric.value,
        source=metric.source,
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


# LIST METRICS (protected)

@router.get("/", response_model=List[MetricResponse])
def list_metrics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    metrics = (
        db.query(Metric)
        .order_by(Metric.created_at.desc())
        .limit(50)
        .all()
    )
    return metrics


# MANUAL COLLECT

@router.post("/collect")
def collect_metrics(db: Session = Depends(get_db)):
    collect_system_metrics(db)
    return {"status": "metrics collected"}


# ALERTS (protected)

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recent = (
        db.query(Metric)
        .order_by(Metric.created_at.desc())
        .limit(50)
        .all()
    )

    alerts = []
    for m in recent:
        severity = detect_spike(db, m.name, m.value)
        if severity:
            alerts.append({
                "metric": m.name,
                "value": m.value,
                "source": m.source,
                "timestamp": m.created_at,
                "severity": severity,
            })

    return {"alerts": alerts}


@router.websocket("/ws")
async def metrics_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            metrics = (
                db.query(Metric)
                .order_by(Metric.created_at.desc())
                .limit(50)
                .all()
            )
            data = [
                {
                    "name": m.name,
                    "value": m.value,
                    "source": m.source,
                    "created_at": m.created_at.isoformat(),
                }
                for m in metrics
            ]
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
