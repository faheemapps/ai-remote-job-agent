"""
Jooble REST API connector -- broad international job-board coverage,
including India/UAE, that plain RSS/Google-News scraping can't reach.

Requires a free JOOBLE_API_KEY (sign up at https://jooble.org/api/about),
set as a GitHub Actions repo secret and passed in via the JOOBLE_API_KEY
environment variable. If the key isn't set, this raises RuntimeError,
which main.py's collect_free_apis()-style caller should catch so a missing
key here never stops the other sources from running.
"""
import os
import requests
from .free_apis import clean_html, to_iso8601, QUERY
from ..models import Job

HEADERS = {"User-Agent": "AI-Remote-Job-Agent/1.0 (personal use)"}
TIMEOUT = 25


def fetch_jooble(limit=25):
    api_key = os.environ.get("JOOBLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "JOOBLE_API_KEY not set -- sign up free at https://jooble.org/api/about "
            "and add the key as a GitHub Actions repo secret"
        )

    url = f"https://jooble.org/api/{api_key}"
    r = requests.post(url, json={"keywords": QUERY, "location": ""}, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()

    jobs = []
    for j in r.json().get("jobs", [])[:limit]:
        jobs.append(Job(
            title=j.get("title", ""), company=j.get("company", "Unknown"),
            location=j.get("location") or "Remote",
            url=j.get("link", ""), description=clean_html(j.get("snippet", "")),
            salary=j.get("salary") or None,
            posted_at=to_iso8601(j.get("updated")),
            source="Jooble", remote=True,
        ))
    return jobs
