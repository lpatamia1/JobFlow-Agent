# app/agents/orchestrator.py
from .scraper_agent import ScraperAgent
from .writer_agent import WriterAgent
from .reminder_agent import ReminderAgent

class Orchestrator:
    def __init__(self, db):
        self.db = db

    def run_writer(self, job_id: int, resume_id: int):
        agent = WriterAgent(self.db)
        return agent.run(job_id=job_id, resume_id=resume_id)

    def run_reminder(self):
        agent = ReminderAgent(self.db)
        return agent.run()
