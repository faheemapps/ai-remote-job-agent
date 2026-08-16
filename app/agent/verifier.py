from ..agent.recruiter import extract_contacts

def verify(job):
    text = f"{job.title} {job.location} {job.description}".lower()
    negative = [
        "us work authorization required", "u.s. only", "must be located in the us",
        "must reside in uae", "uae residence required", "uk only"
    ]
    positive = [
        "worldwide remote", "remote worldwide", "work from anywhere",
        "remote india", "india remote", "remote - india", "global remote"
    ]
    if any(x in text for x in negative):
        job.remote_from_india = False
    elif any(x in text for x in positive):
        job.remote_from_india = True
    else:
        job.remote_from_india = None
    contacts = extract_contacts(job.description)
    if contacts["emails"]:
        job.recruiter_email = contacts["emails"][0]
    if contacts["phones"]:
        job.recruiter_phone = contacts["phones"][0]
    return job
