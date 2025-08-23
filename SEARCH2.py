import asyncio
from playwright.async_api import async_playwright
import pandas as pd


async def scrape_naukri(job_title="Data Scientist", location="Mumbai"):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # True = headless
        context = await browser.new_context()
        page = await context.new_page()

        search_url = f"https://www.naukri.com/{job_title.replace(' ', '-')}-jobs-in-{location}"
        await page.goto(search_url, timeout=60000)

        await page.wait_for_selector(".cust-job-tuple")
        job_cards = await page.query_selector_all(".cust-job-tuple")

        for card in job_cards[:20]:
            title = await card.query_selector(".title")
            company = await card.query_selector(".subTitle")
            experience = await card.query_selector(".expwdth")
            salary = await card.query_selector(".salary")
            loc = await card.query_selector(".locWdth")

            results.append({
                "source": "Naukri",
                "title": await title.inner_text() if title else None,
                "company": await company.inner_text() if company else None,
                "experience": await experience.inner_text() if experience else None,
                "salary": await salary.inner_text() if salary else None,
                "location": await loc.inner_text() if loc else None,
            })

        await browser.close()
    return results


async def scrape_timesjobs(job_title="Data Scientist", location="Bangalore"):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        search_url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={job_title}&txtLocation={location}"
        await page.goto(search_url, timeout=60000)

        await page.wait_for_selector("li.clearfix.job-bx")
        job_cards = await page.query_selector_all("li.clearfix.job-bx")

        for card in job_cards[:20]:
            title = await card.query_selector("h2 a")
            company = await card.query_selector(".company-name")
            loc = await card.query_selector(".top-jd-dtl li span")
            exp = await card.query_selector(".top-jd-dtl li span.exp")

            results.append({
                "source": "TimesJobs",
                "title": await title.inner_text() if title else None,
                "company": await company.inner_text() if company else None,
                "experience": await exp.inner_text() if exp else None,
                "salary": None,  # TimesJobs doesn’t always list salary openly
                "location": await loc.inner_text() if loc else None,
            })

        await browser.close()
    return results


async def main():
    naukri_jobs = await scrape_naukri("Python Developer", "Mumbai")
    times_jobs = await scrape_timesjobs("Python Developer", "Mumbai")

    all_jobs = naukri_jobs + times_jobs

    df = pd.DataFrame(all_jobs)
    df.to_csv("jobs.csv", index=False, encoding="utf-8")
    print(f"Saved {len(df)} jobs into jobs.csv")


if __name__ == "__main__":
    asyncio.run(main())
