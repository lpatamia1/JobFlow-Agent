# app/services/scraping_service.py
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

class ScrapedJob(BaseModel):
    title: str
    company_name: str
    company_website: str | None = None
    company_location: str | None = None
    location: str | None = None
    raw_description: str
    cleaned_description: str
    salary_min: float | None = None
    salary_max: float | None = None


def scrape_job_posting(url: str) -> ScrapedJob:
    # super basic placeholder, you’ll refine per site
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.find("title").get_text(strip=True)
    description_text = soup.get_text(separator="\n")
    # TODO: heuristics / regex for salary
    return ScrapedJob(
        title=title,
        company_name="Unknown Company",
        company_website=None,
        company_location=None,
        location=None,
        raw_description=description_text,
        cleaned_description=description_text[:8000],
    )
