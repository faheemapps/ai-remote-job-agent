"""
No-signup, no-cost public JSON APIs for remote jobs. These actually index
real job-board listings (unlike the Google News RSS search in
google_news.py, which only sees news articles, and unlike LinkedIn/Naukri,
which block scraping and require login). A connector failing here never
stops the others -- same non-fatal pattern as the other sources.
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from ..models import Job

HEADERS = {"User-Agent": "AI-Remote-Job-Agent/1.0 (personal use)"}
TIMEOUT = 25

# Search text built from the candidate's core stack -- used by the sources
# below that support free-text search or client-side filtering.
QUERY = "Snowflake Informatica ETL data warehouse PL/SQL"
Q_TERMS = [t.lower() for t in QUERY.replace("/", " ").split()]


def clean_html(value):
    return BeautifulSoup(value or "", "html.parser").get_text(" ", strip=True)


def to_iso8601(value):
    """Normalize a date field that may be an ISO string, a unix timestamp
    (seconds or milliseconds), or missing, into an ISO8601 string or None.
    Never raises -- unparseable values become None."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        try:
            seconds = value / 1000 if value > 10**11 else value
            return datetime.fromtimestamp(seconds, tz=timezone.utc).isoformat()
        except (ValueError, OSError, OverflowError):
            return None
    if isinstance(value, str):
        return value
    return None


def _matches(text):
    text = text.lower()
    return any(t in text for t in Q_TERMS)


def fetch_remotive(limit=25):
    r = requests.get("https://remotive.com/api/remote-jobs",
                      params={"search": QUERY, "limit": limit}, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    jobs = []
    for j in r.json().get("jobs", []):
        jobs.append(Job(
            title=j.get("title", ""), company=j.get("company_name", "Unknown"),
            location=j.get("candidate_required_location") or "Remote",
            url=j.get("url", ""), description=clean_html(j.get("description", "")),
            salary=j.get("salary") or None,
            posted_at=to_iso8601(j.get("publication_date")),
            source="Remotive", remote=True,
        ))
    return jobs


def fetch_remoteok(limit=25):
    r = requests.get("https://remoteok.com/api", headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    jobs = []
    for j in r.json():
        if not isinstance(j, dict) or "position" not in j:
            continue
        text = f"{j.get('position','')} {j.get('description','')}"
        if not _matches(text):
            continue
        jobs.append(Job(
            title=j.get("position", ""), company=j.get("company", "Unknown"),
            location=j.get("location") or "Remote",
            url=(f"https://remoteok.com/remote-jobs/{j.get('id')}" if j.get("id") else j.get("url", "")),
            description=clean_html(j.get("description", "")),
            salary=(f"{j.get('salary_min','')}-{j.get('salary_max','')}" if j.get("salary_min") else None),
            posted_at=to_iso8601(j.get("date")),
            source="RemoteOK", remote=True,
        ))
        if len(jobs) >= limit:
            break
    return jobs


def fetch_arbeitnow(limit=25):
    r = requests.get("https://www.arbeitnow.com/api/job-board-api", headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    jobs = []
    for j in r.json().get("data", []):
        text = f"{j.get('title','')} {j.get('description','')}"
        if not _matches(text):
            continue
        jobs.append(Job(
            title=j.get("title", ""), company=j.get("company_name", "Unknown"),
            location=j.get("location") or ("Remote" if j.get("remote") else ""),
            url=j.get("url", ""), description=clean_html(j.get("description", "")),
            salary=None, posted_at=None,
            source="Arbeitnow", remote=True,
        ))
        if len(jobs) >= limit:
            break
    return jobs


def fetch_jobicy(limit=25):
    r = requests.get("https://jobicy.com/api/v2/remote-jobs",
                      params={"count": limit, "tag": "data"}, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    jobs = []
    for j in r.json().get("jobs", []):
        salary = None
        if j.get("annualSalaryMin"):
            salary = f"{j.get('annualSalaryMin')}-{j.get('annualSalaryMax')} {j.get('salaryCurrency','')}"
        jobs.append(Job(
            title=j.get("jobTitle", ""), company=j.get("companyName", "Unknown"),
            location=j.get("jobGeo") or "Remote",
            url=j.get("url", ""), description=clean_html(j.get("jobExcerpt", "")),
            salary=salary, posted_at=to_iso8601(j.get("pubDate")),
            source="Jobicy", remote=True,
        ))
    return jobs


def fetch_himalayas(limit=25):
    r = requests.get("https://himalayas.app/jobs/api", params={"limit": limit}, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    jobs = []
    for j in r.json().get("jobs", []):
        company = j.get("companyName") or (j.get("company") or {}).get("name") or "Unknown"
        jobs.append(Job(
            title=j.get("title", ""), company=company,
            location=", ".join(j.get("locationRestrictions", []) or []) or "Remote",
            url=j.get("applicationLink") or j.get("guid") or "",
            description=clean_html(j.get("description", "")),
            salary=None, posted_at=to_iso8601(j.get("pubDate")),
            source="Himalayas", remote=True,
        ))
    return jobs


def fetch_themuse(limit=25):
    jobs = []
    for category in ("Data Science", "Engineering"):
        for page in range(2):
            r = requests.get("https://www.themuse.com/api/public/jobs",
                              params={"category": category, "page": page}, headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            results = r.json().get("results", [])
            if not results:
                break
            for j in results:
                text = f"{j.get('name','')} {clean_html(j.get('contents',''))}"
                if not _matches(text):
                    continue
                locations = j.get("locations") or []
                jobs.append(Job(
                    title=j.get("name", ""),
                    company=(j.get("company") or {}).get("name", "Unknown"),
                    location=", ".join(l.get("name", "") for l in locations) or "Remote",
                    url=(j.get("refs") or {}).get("landing_page", ""),
                    description=clean_html(j.get("contents", "")),
                    salary=None, posted_at=to_iso8601(j.get("publication_date")),
                    source="TheMuse", remote=True,
                ))
                if len(jobs) >= limit:
                    return jobs
    return jobs


FETCHERS = [fetch_remotive, fetch_remoteok, fetch_arbeitnow, fetch_jobicy, fetch_himalayas, fetch_themuse]


def collect_free_apis():
    """Calls every free-API source; one failing never stops the others."""
    jobs = []
    for fn in FETCHERS:
        try:
            jobs.extend(fn())
        except Exception as exc:  # noqa: BLE001 - intentionally broad, logged not raised
            print(f"[WARN] {fn.__name__}: {exc}")
    return jobs
