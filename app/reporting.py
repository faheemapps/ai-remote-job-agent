import html
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def build_report(rows):
    parts = [
        "<h2>AI Remote Job Agent</h2>",
        f"<p>Top matching jobs: {len(rows)}</p>",
        "<table border='1' cellpadding='6' cellspacing='0'>",
        "<tr>"
        "<th>Score</th>"
        "<th>Company</th>"
        "<th>Role</th>"
        "<th>Location</th>"
        "<th>Source</th>"
        "<th>Contact</th>"
        "<th>Apply</th>"
        "</tr>",
    ]

    for job, result in rows:
        contact = "<br>".join(
            x for x in [
                job.recruiter_email,
                job.recruiter_phone
            ] if x
        ) or "-"

        parts.append(
            f"<tr>"
            f"<td>{result['score']}%</td>"
            f"<td>{html.escape(job.company)}</td>"
            f"<td>{html.escape(job.title)}</td>"
            f"<td>{html.escape(job.location or 'Remote/Unspecified')}</td>"
            f"<td>{html.escape(job.source)}</td>"
            f"<td>{html.escape(contact)}</td>"
            f"<td><a href='{html.escape(job.url)}'>Open</a></td>"
            f"</tr>"
        )

    parts.append("</table>")
    return "".join(parts)


def send(rows):

    print("========================================")
    print("EMAIL CONFIGURATION CHECK")
    print("========================================")

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    report_email = os.getenv("REPORT_EMAIL")

    print(f"SMTP_HOST configured: {bool(smtp_host)}")
    print(f"SMTP_PORT configured: {bool(smtp_port)}")
    print(f"SMTP_USERNAME configured: {bool(smtp_username)}")
    print(f"SMTP_PASSWORD configured: {bool(smtp_password)}")
    print(f"REPORT_EMAIL configured: {bool(report_email)}")
    print(f"Jobs in report: {len(rows)}")

    if not report_email:
        raise RuntimeError(
            "REPORT_EMAIL GitHub Secret is missing or was not passed to the workflow."
        )

    if not smtp_username:
        raise RuntimeError(
            "SMTP_USERNAME GitHub Secret is missing."
        )

    if not smtp_password:
        raise RuntimeError(
            "SMTP_PASSWORD GitHub Secret is missing."
        )

    if not smtp_host:
        raise RuntimeError(
            "SMTP_HOST GitHub Secret is missing."
        )

    if not smtp_port:
        smtp_port = "587"

    message = MIMEMultipart("alternative")

    message["Subject"] = "AI Job Agent — Daily Matches"
    message["From"] = smtp_username
    message["To"] = report_email

    message.attach(
        MIMEText(build_report(rows), "html")
    )

    print("Connecting to Gmail SMTP...")

    try:
        with smtplib.SMTP(
            smtp_host,
            int(smtp_port),
            timeout=30
        ) as server:

            print("Starting TLS...")
            server.starttls()

            print("Logging into Gmail...")
            server.login(
                smtp_username,
                smtp_password
            )

            print("Sending email...")

            server.sendmail(
                smtp_username,
                report_email,
                message.as_string()
            )

        print("========================================")
        print("EMAIL SENT SUCCESSFULLY")
        print("========================================")

    except Exception as e:
        print("========================================")
        print("EMAIL FAILED")
        print(f"Error: {type(e).__name__}: {e}")
        print("========================================")
        raise
