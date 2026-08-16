import urllib.parse
import feedparser
from ..models import Job

# This adapter uses Google's public RSS search endpoint for discovery.
# It does not log in, bypass CAPTCHA, or scrape private content.
QUERIES = [
    ('LinkedIn Jobs', '"Snowflake" "Informatica" "PL/SQL" remote job'),
    ('LinkedIn Jobs UAE', 'site:linkedin.com/jobs Snowflake Informatica Dubai remote'),
    ('Naukri', 'site:naukri.com/job-listings Snowflake Informatica PL/SQL remote'),
    ('Naukri Gulf', 'site:naukrigulf.com Snowflake Informatica PL/SQL Dubai'),
    ('Indeed', 'site:indeed.com/viewjob Snowflake Informatica PL/SQL remote'),
    ('Deloitte Careers', 'site:deloitte.com careers Snowflake Informatica remote'),
    ('Accenture Careers', 'site:accenture.com careers Snowflake Informatica remote'),
    ('Cognizant Careers', 'site:cognizant.com careers Snowflake Informatica remote'),
    ('Capgemini Careers', 'site:capgemini.com careers Snowflake Informatica remote'),
    ('TCS Careers', 'site:tcs.com careers Snowflake Informatica data engineer'),
    ('Infosys Careers', 'site:infosys.com careers Snowflake Informatica'),
    ('HCLTech Careers', 'site:hcltech.com careers Snowflake Informatica'),
    ('Wipro Careers', 'site:wipro.com careers Snowflake Informatica'),
]

BASE = "https://news.google.com/rss/search?q={}&hl=en-IN&gl=IN&ceid=IN:en"

def collect_google_news():
    jobs = []
    for source, query in QUERIES:
        try:
            url = BASE.format(urllib.parse.quote(query))
            feed = feedparser.parse(url)
            for e in feed.entries:
                jobs.append(Job(
                    title=e.get("title", ""),
                    company=source,
                    location="",
                    url=e.get("link", ""),
                    description=e.get("summary", ""),
                    posted_at=e.get("published", ""),
                    source=source,
                    remote="remote" in e.get("title", "").lower()
                ))
        except Exception as exc:
            print(f"[WARN] {source}: {exc}")
    return jobs
