"""
Simple anomaly detection for OpsLens.

Detection order:
1) Hard thresholds
2) Statistical spike detection
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.metric import Metric

# =========================
# Hard thresholds
# =========================
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 90


def detect_spike(db: Session, metric_name: str, value: float) -> str | None:
    """
    Returns severity level if anomalous, otherwise None.
    """

    # -------------------------
    # Hard threshold alerts
    # -------------------------
    if metric_name == "cpu_usage":
        if value > 90:
            return "critical"
        if value > 80:
            return "warning"

    if metric_name == "memory_usage":
        if value > 95:
            return "critical"
        if value > 90:
            return "warning"

    # -------------------------
    # Statistical fallback
    # -------------------------
    subquery = (
        db.query(Metric.value)
        .filter(Metric.name == metric_name)
        .order_by(Metric.created_at.desc())
        .limit(20)
        .subquery()
    )

    avg = db.query(func.avg(subquery.c.value)).scalar()

    if avg is None:
        return None

    if value > (2 * avg):
        return "warning"

    return None