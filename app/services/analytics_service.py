# app/services/analytics_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Application, JobPosting

def compute_overview_stats(db: Session) -> dict:
    total = db.query(func.count(Application.id)).scalar()
    by_status = dict(
        db.query(Application.status, func.count(Application.id)).group_by(Application.status)
    )
    # apps per week (very rough)
    apps_by_week = db.query(
        func.strftime("%Y-%W", Application.date_applied), func.count(Application.id)
    ).group_by(func.strftime("%Y-%W", Application.date_applied)).all()

    apps_per_week = {week: count for week, count in apps_by_week}

    return {
        "total": total,
        "by_status": by_status,
        "apps_per_week": apps_per_week,
    }
