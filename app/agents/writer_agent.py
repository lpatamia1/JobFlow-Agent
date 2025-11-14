# app/agents/writer_agent.py
from .base_agent import BaseAgent
from ..models import JobPosting, Resume
from sqlalchemy.orm import Session
import os

load_dotenv()

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class WriterAgent(BaseAgent):
    name = "writer-agent"

    def __init__(self, db: Session):
        self.db = db

    def run(self, job_id: int, resume_id: int, tone: str = "concise"):
        job: JobPosting = self.db.query(JobPosting).get(job_id)
        resume: Resume = self.db.query(Resume).get(resume_id)

        prompt = f"""
You are an assistant that writes tailored resume bullet points for job applications.

Job Title: {job.title}
Company: {job.company.name if job.company else 'Unknown'}
Location: {job.location}
Job Description:
{job.cleaned_description[:6000]}

Candidate Resume:
{resume.content[:6000]}

Write 3-5 bullet points in the candidate's voice that:
- Mirror the job description's language.
- Emphasize impact, metrics, and relevant tools.
- Stay {tone} and professional.
- Use past-tense action verbs.

Return ONLY the bullet points as Markdown list items.
"""

        completion = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        bullets_md = completion.choices[0].message["content"]
        return {"tailored_bullets": bullets_md}
