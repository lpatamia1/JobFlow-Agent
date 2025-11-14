# app/routers/agents.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..db import get_db
from ..agents.orchestrator import Orchestrator

router = APIRouter()

class WriterRequest(BaseModel):
    job_id: int
    resume_id: int

@router.post("/writer/tailored-bullets")
def generate_tailored_bullets(payload: WriterRequest, db: Session = Depends(get_db)):
    orch = Orchestrator(db)
    result = orch.run_writer(job_id=payload.job_id, resume_id=payload.resume_id)
    return result


@router.get("/reminder/next-actions")
def get_next_actions(db: Session = Depends(get_db)):
    orch = Orchestrator(db)
    return orch.run_reminder()
