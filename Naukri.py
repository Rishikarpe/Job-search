import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def scrape_naukri(job_title="Data Scientist", location="Mumbai"):
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set True for headless
        context = await browser.new_context()
        page = await context.new_page()

        # Open Naukri search page
        search_url = f"https://www.naukri.com/{job_title.replace(' ', '-')}-jobs-in-{location}"
        await page.goto(search_url, timeout=60000)

        # Wait for job cards to load
        await page.wait_for_selector(".cust-job-tuple")

        job_cards = await page.query_selector_all(".cust-job-tuple")

        for card in job_cards[:20]:  # limit to first 10 results for demo
            title = await card.query_selector(".title")
            company = await card.query_selector(".subTitle")
            experience = await card.query_selector(".expwdth")
            salary = await card.query_selector(".salary")
            location = await card.query_selector(".locWdth")

            results.append({
                "title": await title.inner_text() if title else None,
                "company": await company.inner_text() if company else None,
                "experience": await experience.inner_text() if experience else None,
                "salary": await salary.inner_text() if salary else None,
                "location": await location.inner_text() if location else None,
            })

        await browser.close()

        df = pd.DataFrame(results)
        df.to_csv("jobs.csv", index=False, encoding="utf-8")
        print(f"Saved {len(df)}")

    return results


if __name__ == "__main__":
    jobs = asyncio.run(scrape_naukri("Python Developer", "Mumbai"))
    for i, job in enumerate(jobs, start=1):
        print(f"{i}. {job}")
