"""
Metric model.

Core OpsLens data table.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.db.session import Base


class Metric(Base):
    """
    Stores operational metrics.
    """

    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)

    # Metric name (cpu_usage, latency, revenue, etc.)
    name = Column(String, index=True, nullable=False)

    # Numeric value
    value = Column(Float, nullable=False)

    # Optional source
    source = Column(String, nullable=True)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
