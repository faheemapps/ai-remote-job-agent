import html, os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def build_report(rows):
    parts = ["<h2>AI Remote Job Agent</h2>",
             f"<p>Top matching jobs: {len(rows)}</p>",
             "<table border='1' cellpadding='6' cellspacing='0'>",
             "<tr><th>Score</th><th>Company</th><th>Role</th><th>Location</th><th>Source</th><th>Contact</th><th>Apply</th></tr>"]
    for j, r in rows:
        contact = "<br>".join(x for x in [j.recruiter_email, j.recruiter_phone] if x) or "-"
        parts.append(
            f"<tr><td>{r['score']}%</td><td>{html.escape(j.company)}</td>"
            f"<td>{html.escape(j.title)}</td><td>{html.escape(j.location or 'Remote/Unspecified')}</td>"
            f"<td>{html.escape(j.source)}</td><td>{html.escape(contact)}</td>"
            f"<td><a href='{html.escape(j.url)}'>Open</a></td></tr>")
    parts.append("</table>")
    return "".join(parts)

def send(rows):
    if not os.getenv("REPORT_EMAIL"):
        return
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "AI Job Agent — Daily Matches"
    msg["From"] = os.environ["SMTP_USERNAME"]
    msg["To"] = os.environ["REPORT_EMAIL"]
    msg.attach(MIMEText(build_report(rows), "html"))
    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.getenv("SMTP_PORT", "587"))) as s:
        s.starttls()
        s.login(os.environ["SMTP_USERNAME"], os.environ["SMTP_PASSWORD"])
        s.sendmail(msg["From"], msg["To"], msg.as_string())
