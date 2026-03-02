"""
Metrics API routes.

Provides:
- POST /metrics → ingest data
- GET /metrics → list data
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.metric import Metric
from app.schemas.metric import MetricCreate, MetricResponse
from app.core.analytics import detect_spike
from app.core.collector import collect_system_metrics

router = APIRouter(prefix="/metrics", tags=["metrics"])



# CREATE METRIC

@router.post("/", response_model=MetricResponse)
def create_metric(metric: MetricCreate, db: Session = Depends(get_db)):
    """
    Create a new metric entry.
    """
    db_metric = Metric(
        name=metric.name,
        value=metric.value,
        source=metric.source,
    )

    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)

    return db_metric



# LIST METRICS

@router.get("/", response_model=List[MetricResponse])
def list_metrics(db: Session = Depends(get_db)):
    """
    Return recent metrics.
    """
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
    """
    Manually trigger system metric collection.
    """
    collect_system_metrics(db)
    return {"status": "metrics collected"}



# ALERTS

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    """
    Returns recent metrics that look anomalous.
    """
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
            alert = {
                "metric": m.name,
                "value": m.value,
                "source": m.source,
                "timestamp": m.created_at,
                "severity": severity,
            }
            alerts.append(alert)

    return {"alerts": alerts}