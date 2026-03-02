"""
Background metric scheduler.
Runs system collection every 5 seconds.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from app.core.collector import collect_system_metrics
from app.db.session import SessionLocal

scheduler = BackgroundScheduler()
_scheduler_started = False


def start_scheduler():
    global _scheduler_started

    if _scheduler_started:
        return  # prevents duplicate schedulers

    def job():
        db = SessionLocal()
        try:
            collect_system_metrics(db)
        finally:
            db.close()

    scheduler.add_job(job, "interval", seconds=5)
    scheduler.start()

    _scheduler_started = True