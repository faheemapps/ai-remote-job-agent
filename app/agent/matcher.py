import re
from datetime import datetime, timezone

def norm(s):
    return re.sub(r"\s+", " ", (s or "").lower())

PRIMARY = ["snowflake", "informatica powercenter", "informatica", "oracle pl/sql", "pl/sql", "etl", "data warehouse"]
SECONDARY = ["control-m", "control m", "oracle", "sql", "aws", "python", "microsoft fabric", "airflow", "idmc", "iics", "unix", "data migration", "performance tuning"]
SENIOR = ["senior", "lead", "architect", "principal", "staff", "manager", "director"]

def score(job, profile):
    text = norm(f"{job.title} {job.company} {job.location} {job.description}")
    primary = [x for x in PRIMARY if norm(x) in text]
    secondary = [x for x in SECONDARY if norm(x) in text]
    senior = any(x in text for x in SENIOR)
    remote = job.remote or "remote" in text or "work from home" in text

    value = min(60, round(len(primary) / len(PRIMARY) * 60))
    value += min(15, round(len(secondary) / len(SECONDARY) * 15))
    value += 10 if senior else 0
    value += 10 if remote else 0

    if "dubai" in text or "uae" in text:
        value += 5

    return {
        "score": min(100, value),
        "primary": primary,
        "secondary": secondary,
        "senior": senior,
        "remote": remote,
    }

def within_days(job, days):
    if not job.posted_at:
        return True
    try:
        raw = job.posted_at.replace("Z", "+00:00")
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).total_seconds() <= days * 86400
    except Exception:
        return True
