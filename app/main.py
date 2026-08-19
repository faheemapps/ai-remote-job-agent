from .config import PROFILE
from .sources.rss import collect_rss
from .sources.google_news import collect_google_news
from .sources.company_sites import collect_company_pages
from .sources.free_apis import collect_free_apis
from .sources.Jooble import fetch_jooble
from .agent.matcher import score, within_days
from .agent.verifier import verify
from .database import save
from .reporting import send

def collect_jooble():
    """Jooble needs an API key -- skip it (not crash the run) if it's not
    configured yet, same non-fatal pattern as every other source."""
    try:
        return fetch_jooble()
    except Exception as exc:  # noqa: BLE001 - intentionally broad, logged not raised
        print(f"[WARN] Jooble: {exc}")
        return []

def main():
    jobs = collect_rss() + collect_google_news() + collect_company_pages() + collect_free_apis() + collect_jooble()
    print(f"Discovered: {len(jobs)}")

    unique = {}
    for j in jobs:
        if j.url:
            unique[j.url] = j

    rows = []
    for j in unique.values():
        if not within_days(j, PROFILE["job_age"]["maximum_days"]):
            continue
        j = verify(j)
        if j.remote_from_india is False:
            continue
        result = score(j, PROFILE)
        if result["score"] < PROFILE["matching"]["minimum_score"]:
            continue
        save(j, result["score"])
        rows.append((j, result))

    rows.sort(key=lambda x: x[1]["score"], reverse=True)
    rows = rows[:20]
    for j, r in rows:
        print(f"{r['score']:>3}% | {j.company} | {j.title} | {j.source} | {j.url}")
    send(rows)

if __name__ == "__main__":
    main()
