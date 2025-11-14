# app/agents/reminder_agent.py
from .base_agent import BaseAgent
from sqlalchemy.orm import Session
from ..models import Application
import os, openai
from datetime import datetime, timedelta

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ReminderAgent(BaseAgent):
    name = "reminder-agent"

    def __init__(self, db: Session):
        self.db = db

    def run(self):
        # naive example: find apps older than 7 days with status APPLIED
        cutoff = datetime.utcnow() - timedelta(days=7)
        stale_apps = (
            self.db.query(Application)
            .filter(Application.status == "APPLIED")
            .filter(Application.date_applied < cutoff)
            .all()
        )

        summary_lines = []
        for app in stale_apps:
            summary_lines.append(
                f"- {app.job.title} at {app.job.company.name if app.job.company else ''} "
                f"(applied {app.date_applied.date()})"
            )
        context = "\n".join(summary_lines) or "No stale applications."

        prompt = f"""
Here are job applications that have not been updated in over a week:

{context}

Suggest concrete next actions for the candidate (follow-ups, networking, etc.)
in 3-5 bullet points.
"""

        completion = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        advice = completion.choices[0].message["content"]
        return {"stale_count": len(stale_apps), "advice": advice}
