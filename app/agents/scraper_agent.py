# app/agents/scraper_agent.py
from .base_agent import BaseAgent
from ..services.scraping_service import scrape_job_posting

class ScraperAgent(BaseAgent):
    name = "scraper-agent"

    def run(self, url: str):
        return scrape_job_posting(url)
