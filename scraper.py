import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

def polite_sleep():
    #Sleep random,avoid blocklist
    delay = random.uniform(4, 9)
    print(f"    [sleeping {delay:.1f}s...]")
    time.sleep(delay)
HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/573.36"
        )
}

def scrape_linkedin() -> list[dict]:
    jobs = []
    search_terms = [
            "junior NOC engineer",
            "junior cloud engineer",
            "junior network engineer",
            "junior devops engineer",
            "junior linux"
            "junior system administrator",
            "entry level network",
            "entry level cloud",
    ]

    EXCLUDE = ["senior", "lead", "manager", "principal", "staff", "head of", "architect", "medior"]

    for term in search_terms:
        try:
            url = (
                "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
                f"?keywords={requests.utils.quote(term)}&location=Belgrade%2C+Serbia&start=0"
            )
            resp = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")

            listings = soup.select("li")

            for item in listings[:15]:
                title_el = item.select_one(".base-search-card__title, h3")
                company_el = item.select_one(".base-search-card__subtitle, h4")
                location_el = item.select_one(".base-search-card__location")
                link_el = item.select_one("a[href]")

                title = title_el.get_text(strip=True) if title_el else ""
                company = company_el.get_text(strip=True) if company_el else "N/A"
                location = location_el.get_text(strip=True) if location_el else "Serbia"
                link = link_el["href"].split("?")[0] if link_el else ""

                if not title:
                    continue

                #Skip roles
                if any(ex in title.lower() for ex in EXCLUDE):
                    continue

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": link,
                    "source": "LinkedIn",
                    "date_found": datetime.utcnow().isoformat(),
                })

            polite_sleep()

        except Exception as e:
            print(f"[LinkedIn] Error for '{term}': {e}")
    return deduplicate(jobs)

def deduplicate(jobs: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for job in jobs:
        key = (job["title"].lower().strip(), job["company"].lower().strip())
        if key not in seen:
            seen.add(key)
            unique.append(job)
    return unique

def scrape_all() -> list[dict]:
    print("[*] Scraping LinkedIn...")
    jobs = scrape_linkedin()
    print(f"    {len(jobs)} jobs found")
    print(f"[*] Total: {len(jobs)} jobs scraped")
    return jobs

