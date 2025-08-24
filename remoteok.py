import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://remoteok.com/"

def fetch_jobs():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(BASE_URL, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to fetch jobs")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_table = soup.find("table", {"id": "jobsboard"})
    if not job_table:
        print("❌ Could not find jobs board on page")
        return []

    jobs = []
    job_rows = job_table.find_all("tr", {"class": "job"})

    for job in job_rows:
        try:
            title = job.find("h2", {"itemprop": "title"}).get_text(strip=True)
            company = job.find("h3", {"itemprop": "name"}).get_text(strip=True)
            location = job.find("div", {"class": "location"})
            location = location.get_text(strip=True) if location else "Remote"

            tags = [tag.get_text(strip=True) for tag in job.find_all("span", {"class": "tag"})]
            link = BASE_URL.rstrip("/") + job.get("data-href", "")

            jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Tags": ", ".join(tags),
                "Link": link
            })
        except Exception as e:
            print("⚠️ Skipping a job due to error:", e)

    return jobs


def save_to_csv(jobs, filename="remoteok_jobs.csv"):
    if not jobs:
        print("⚠️ No jobs to save")
        return

    keys = jobs[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs)

    print(f"✅ Saved {len(jobs)} jobs to {filename}")


if __name__ == "__main__":
    print("⏳ Fetching jobs from RemoteOK...")
    jobs = fetch_jobs()
    save_to_csv(jobs)
