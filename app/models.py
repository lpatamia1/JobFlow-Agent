# app/models.py
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Text, ForeignKey, Float, Enum
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    website = Column(String)
    location = Column(String)
    industry = Column(String)
    glassdoor_rating = Column(Float)
    last_refreshed = Column(DateTime, default=datetime.utcnow)

    jobs = relationship("JobPosting", back_populates="company")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)        # "CS Grad general", "IT Support"
    content = Column(Text, nullable=False)        # raw text or markdown
    created_at = Column(DateTime, default=datetime.utcnow)


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    location = Column(String)
    source = Column(String)                       # "LinkedIn", "Indeed"
    raw_description = Column(Text)
    cleaned_description = Column(Text)
    salary_min = Column(Float)
    salary_max = Column(Float)
    currency = Column(String, default="USD")
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")


class ApplicationStatusEnum(str, Enum):
    APPLIED = "APPLIED"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    SAVED = "SAVED"          # saved/PINNED but not applied yet


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_postings.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    status = Column(String, default="APPLIED")
    date_applied = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    tailored_bullets = Column(Text)  # result from Writer Agent
    last_updated = Column(DateTime, default=datetime.utcnow)

    job = relationship("JobPosting", back_populates="applications")
    resume = relationship("Resume")
