import sys
from scraper import scrape_all
from database import init_db, save_new_jobs, get_all_jobs

def cmd_scrape():
    init_db()
    jobs = scrape_all()
    new_jobs = save_new_jobs(jobs)
    print(f"\n[*] {len(new_jobs)} new jobs saved.\n")
    for job in new_jobs:
        print(f"  [{job['source']}] {job['title']} @ {job['company']} ({job['location']})")

def cmd_list():
    init_db()
    jobs = get_all_jobs(limit=100)
    if not jobs:
        print("[*] No jobs yet. Run: python3 main.py scrape")
        return
    print(f"\n{'─'*80}")
    for job in jobs:
        print(f"  [{job['source']:10}] {job['title'][:40]:40} @ {job['company'][:25]}")
    print(f"{'─'*80}")
    print(f"  Total: {len(jobs)} jobs\n")

COMMANDS = {
    "scrape": cmd_scrape,
    "list": cmd_list,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scrape"
    if cmd not in COMMANDS:
        print("Usage: python3 main.py [scrape|list]")
        sys.exit(1)
    COMMANDS[cmd]()
