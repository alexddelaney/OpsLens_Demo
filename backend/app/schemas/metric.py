"""
Metric schemas.

Purpose:
- Validate incoming metric data
- Shape outgoing responses
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MetricCreate(BaseModel):
    """
    Schema for creating a metric.
    """

    name: str
    value: float
    source: Optional[str] = None


class MetricResponse(BaseModel):
    """
    Schema returned to clients.
    """

    id: int
    name: str
    value: float
    source: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  # allows ORM → schema conversion
