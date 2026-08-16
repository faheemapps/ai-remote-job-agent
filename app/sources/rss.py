import feedparser
import requests
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from ..models import Job

FEEDS = {
    "Remote OK": "https://remoteok.com/remote-data-jobs.rss",
    "We Work Remotely": "https://weworkremotely.com/categories/remote-programming-jobs.rss",
    "Remotive": "https://remotive.com/remote-jobs/feed",
    "Jobspresso": "https://jobspresso.co/feed/",
    "Working Nomads": "https://www.workingnomads.com/jobs.rss",
}

def clean_html(value):
    return BeautifulSoup(value or "", "html.parser").get_text(" ", strip=True)

def parse_date(value):
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc)
    except Exception:
        return None

def fetch_feed(name, url):
    r = requests.get(url, timeout=25, headers={"User-Agent": "AI-Remote-Job-Agent/1.0"})
    r.raise_for_status()
    feed = feedparser.parse(r.content)
    out = []
    for e in feed.entries:
        title = e.get("title", "").strip()
        link = e.get("link", "").strip()
        desc = clean_html(e.get("summary", "") or e.get("description", ""))
        company = e.get("author", "") or e.get("dc_creator", "") or "Unknown"
        published = parse_date(e.get("published", "") or e.get("updated", ""))
        out.append(Job(
            title=title, company=company, location="Remote", url=link,
            description=desc, posted_at=published.isoformat() if published else None,
            source=name, remote=True
        ))
    return out

def collect_rss():
    jobs = []
    for name, url in FEEDS.items():
        try:
            jobs.extend(fetch_feed(name, url))
        except Exception as exc:
            print(f"[WARN] {name}: {exc}")
    return jobs
