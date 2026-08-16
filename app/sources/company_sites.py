import requests
from bs4 import BeautifulSoup
from ..models import Job

# Add permitted public careers/search pages here. The generic adapter only
# extracts ordinary links; it does not bypass login, CAPTCHA or anti-bot controls.
COMPANY_PAGES = {
    "Deloitte": "https://apply.deloitte.com/",
    "Accenture": "https://www.accenture.com/in-en/careers/jobsearch",
    "Cognizant": "https://careers.cognizant.com/global/en",
}

KEYWORDS = ("snowflake", "informatica", "pl/sql", "data engineer", "etl", "data warehouse")

def collect_company_pages():
    jobs = []
    for company, url in COMPANY_PAGES.items():
        try:
            r = requests.get(url, timeout=25, headers={"User-Agent": "AI-Remote-Job-Agent/1.0"})
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a", href=True):
                text = a.get_text(" ", strip=True)
                if not text:
                    continue
                if any(k in text.lower() for k in KEYWORDS):
                    href = a["href"]
                    if href.startswith("/"):
                        from urllib.parse import urljoin
                        href = urljoin(url, href)
                    jobs.append(Job(
                        title=text[:300], company=company, location="",
                        url=href, description=text, source=f"{company} Careers"
                    ))
        except Exception as exc:
            print(f"[WARN] {company} careers page: {exc}")
    return jobs
