"""
System metrics collector.

Collects CPU and memory usage and stores them in the database.
"""

import psutil
from sqlalchemy.orm import Session
from app.models.metric import Metric


def collect_system_metrics(db: Session):
    """
    Collect basic system metrics and store them.
    """

    # CPU usage percentage over 1 second
    cpu = psutil.cpu_percent(interval=1)

    # Memory usage percentage
    memory = psutil.virtual_memory().percent

    metrics = [
        Metric(name="cpu_usage", value=cpu, source="local-agent"),
        Metric(name="memory_usage", value=memory, source="local-agent"),
    ]

    for metric in metrics:
        db.add(metric)

    db.commit()
