# app/routers/jobs.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import JobPosting, Company
from ..services.scraping_service import scrape_job_posting

router = APIRouter()

class JobFromUrlRequest(BaseModel):
    url: HttpUrl
    source: str = "LinkedIn"


@router.post("/from-url")
def create_job_from_url(payload: JobFromUrlRequest, db: Session = Depends(get_db)):
    data = scrape_job_posting(payload.url)

    company = db.query(Company).filter_by(name=data.company_name).first()
    if not company:
        company = Company(
            name=data.company_name,
            website=data.company_website,
            location=data.company_location,
        )
        db.add(company)
        db.flush()

    job = JobPosting(
        url=str(payload.url),
        title=data.title,
        company_id=company.id,
        location=data.location,
        source=payload.source,
        raw_description=data.raw_description,
        cleaned_description=data.cleaned_description,
        salary_min=data.salary_min,
        salary_max=data.salary_max,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job
