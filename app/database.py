import sqlite3
from pathlib import Path

DB = Path("data/jobs.db")

def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY, title TEXT, company TEXT, location TEXT,
        url TEXT UNIQUE, description TEXT, salary TEXT, posted_at TEXT,
        source TEXT, score INTEGER, remote_from_india TEXT,
        recruiter_email TEXT, recruiter_phone TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    c.commit()
    return c

def save(job, score):
    c = connect()
    c.execute("""INSERT OR IGNORE INTO jobs
        (title,company,location,url,description,salary,posted_at,source,score,
         remote_from_india,recruiter_email,recruiter_phone)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
        (job.title,job.company,job.location,job.url,job.description,job.salary,
         job.posted_at,job.source,score,str(job.remote_from_india),
         job.recruiter_email,job.recruiter_phone))
    c.commit()
    c.close()
