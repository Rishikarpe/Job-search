import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from urllib.parse import quote


# -----------------------------
# Scraper for SimplyHired
# -----------------------------
def scrape_simplyhired(job_title, location, num_pages=1):
    jobs = []
    base_url = "https://www.simplyhired.co.in/search?q={job}&l={loc}&pn={page}"
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, num_pages + 1):
        url = base_url.format(job=quote(job_title), loc=quote(location), page=page)
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        postings = soup.find_all("li", class_="css-0")  # Each job card
        for post in postings:
            title_tag = post.find("h2", {"data-testid": "searchSerpJobTitle"})
            summary_tag = post.find("p", {"data-testid": "searchSerpJobSnippet"})
            link_tag = post.find("a", href=True)

            # Sometimes company & location are in sibling divs
            comp_loc_tag = post.find("div", class_="css-1gatmva")

            jobs.append({
                "Title": title_tag.text.strip() if title_tag else None,
                "Company/Location": comp_loc_tag.text.strip() if comp_loc_tag else None,
                "Summary": summary_tag.text.strip() if summary_tag else None,
                "Link": "https://www.simplyhired.co.in" + link_tag["href"] if link_tag else None,
                "Source": "SimplyHired"
            })
    return jobs


# -----------------------------
# Scraper for TimesJobs
# -----------------------------
def scrape_timesjobs(job_title, location, num_pages=1):
    jobs = []
    base_url = ("https://www.timesjobs.com/candidate/job-search.html?"
                "searchType=personalizedSearch&from=submit&txtKeywords={job}"
                "&txtLocation={loc}&sequence={page}&startPage={page}")
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, num_pages + 1):
        url = base_url.format(job=quote(job_title), loc=quote(location), page=page)
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        postings = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
        for post in postings:
            title_tag = post.find("h2").a if post.find("h2") else None
            company = post.find("h3", class_="joblist-comp-name")
            location_tag = post.find("ul", class_="top-jd-dtl clearfix")
            summary = post.find("ul", class_="list-job-dtl clearfix")

            jobs.append({
                "Title": title_tag.text.strip() if title_tag else None,
                "Company": company.text.strip() if company else None,
                "Location": location_tag.li.text.strip() if location_tag and location_tag.li else None,
                "Summary": summary.li.text.strip() if summary and summary.li else None,
                "Link": title_tag["href"] if title_tag and title_tag.has_attr("href") else None,
                "Source": "TimesJobs"
            })
    return jobs


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Job Aggregator", layout="wide")
st.title("Job Posting Aggregator")
st.write("Scrape jobs from **SimplyHired** and **TimesJobs** 🚀")

job_title = st.text_input("Enter Job Title:", "Data Scientist")
location = st.text_input("Enter Location:", "Mumbai")
num_pages = st.slider("Number of Pages to Scrape:", 1, 5, 1)

if st.button("Scrape Jobs"):
    st.info("Scraping jobs... please wait ⏳")

    simplyhired_jobs = scrape_simplyhired(job_title, location, num_pages)
    timesjobs_jobs = scrape_timesjobs(job_title, location, num_pages)

    all_jobs = simplyhired_jobs + timesjobs_jobs
    df = pd.DataFrame(all_jobs)

    st.success(f"✅ Scraped {len(df)} jobs")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "jobs.csv", "text/csv")
