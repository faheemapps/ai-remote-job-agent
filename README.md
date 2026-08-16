# AI Remote Job Agent — Multi Source

Automated multi-source job discovery for:
**Snowflake + Oracle PL/SQL + Informatica PowerCenter + ETL/Data Warehouse + Control-M + Fabric/Airflow**.

## Sources

### Direct public feeds
- Remote OK
- We Work Remotely
- Remotive
- Jobspresso
- Working Nomads

### Discovery feeds
Google News RSS queries are used to discover publicly indexed job pages for:
- LinkedIn Jobs
- Naukri
- Naukri Gulf
- Indeed
- Deloitte Careers
- Accenture Careers
- Cognizant Careers
- Capgemini Careers
- TCS Careers
- Infosys Careers
- HCLTech Careers
- Wipro Careers

### Company pages
A configurable public-careers adapter is included for selected company career pages.

## Important source limitation

This project does NOT log into LinkedIn/Naukri/Indeed, bypass CAPTCHAs, evade anti-bot systems, or access private APIs without authorization. Discovery sources may return an indexed result rather than the canonical job page. Add official APIs/feeds only where you have permission.

## Scheduling

GitHub Actions runs at:
- 06:47 IST
- 12:47 IST
- 18:47 IST

You can also run it manually from Actions.

## Gmail

Use a Google App Password in GitHub Actions secrets:
SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, REPORT_EMAIL.

Never commit the App Password.

## Deployment

```bash
git init
git add .
git commit -m "Initial multi-source AI job agent"
git branch -M main
git remote add origin https://github.com/faheemapps/ai-remote-job-agent.git
git push -u origin main
```

Then:
GitHub -> Settings -> Secrets and variables -> Actions

Add:
SMTP_HOST
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
REPORT_EMAIL

Then:
Actions -> Multi-Source AI Job Agent -> Run workflow

## Future upgrades

- Official partner APIs where credentials/permissions exist
- LLM-based semantic matching
- CV parsing and per-job CV tailoring
- recruiter/public contact enrichment
- salary normalization to INR/AED/USD
- 24-hour strict freshness scoring
- application tracker
- Telegram/WhatsApp notification
