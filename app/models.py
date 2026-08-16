from dataclasses import dataclass
from typing import Optional

@dataclass
class Job:
    title: str
    company: str
    location: str
    url: str
    description: str = ""
    salary: Optional[str] = None
    posted_at: Optional[str] = None
    source: str = ""
    remote: bool = False
    remote_from_india: Optional[bool] = None
    recruiter_name: Optional[str] = None
    recruiter_email: Optional[str] = None
    recruiter_phone: Optional[str] = None
