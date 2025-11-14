# app/routers/applications.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
from ..db import get_db
from ..models import Application, JobPosting, Resume
from ..services.analytics_service import compute_overview_stats

router = APIRouter()


class ApplicationCreate(BaseModel):
    job_id: int
    resume_id: int
    status: str = "APPLIED"
    notes: Optional[str] = None


@router.post("/", response_model=dict)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    app_obj = Application(
        job_id=payload.job_id,
        resume_id=payload.resume_id,
        status=payload.status,
        notes=payload.notes,
        date_applied=datetime.utcnow(),
    )
    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)
    return {"id": app_obj.id, "status": app_obj.status}


@router.get("/stats/overview")
def get_overview_stats(db: Session = Depends(get_db)):
    return compute_overview_stats(db)
