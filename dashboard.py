import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# -------------------------------
# Function to scrape Naukri
# -------------------------------
def scrape_naukri(job_title, location, num_pages=1):
    jobs = []
    for page in range(1, num_pages + 1):
        url = f"https://www.naukri.com/{job_title.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}-{page}?k={job_title}&l={location}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        job_cards = soup.find_all("article", class_="jobTuple bgWhite br4 mb-8")
        for job in job_cards:
            title = job.find("a", class_="title")
            company = job.find("a", class_="subTitle ellipsis fleft")
            location_tag = job.find("li", class_="fleft grey-text br2 placeHolderLi location")
            salary_tag = job.find("li", class_="fleft grey-text br2 placeHolderLi salary")
            exp_tag = job.find("li", class_="fleft grey-text br2 placeHolderLi experience")

            jobs.append({
                "Title": title.text.strip() if title else "N/A",
                "Company": company.text.strip() if company else "N/A",
                "Location": location_tag.text.strip() if location_tag else "N/A",
                "Salary": salary_tag.text.strip() if salary_tag else "N/A",
                "Experience": exp_tag.text.strip() if exp_tag else "N/A",
                "Link": title["href"] if title else "N/A"
            })
    return jobs


# -------------------------------
# Function to scrape TimesJobs
# -------------------------------
def scrape_timesjobs(job_title, location, num_pages=1):
    jobs = []
    for page in range(1, num_pages + 1):
        url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={job_title}&txtLocation={location}&sequence={page}&startPage=1"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        job_cards = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
        for job in job_cards:
            title = job.find("h2").a
            company = job.find("h3", class_="joblist-comp-name")
            location_tag = job.find("ul", class_="top-jd-dtl clearfix").li
            posted_date = job.find("span", class_="sim-posted")

            jobs.append({
                "Title": title.text.strip() if title else "N/A",
                "Company": company.text.strip() if company else "N/A",
                "Location": location_tag.text.strip() if location_tag else "N/A",
                "Posted": posted_date.text.strip() if posted_date else "N/A",
                "Link": title["href"] if title else "N/A"
            })
    return jobs


# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Job Posting Aggregator 🔎")
st.markdown("Fetch job postings from **Naukri.com** and **TimesJobs.com**")

# Input fields
job_title = st.text_input("Enter Job Title (e.g., Data Scientist)", "Data Scientist")
location = st.text_input("Enter Location (e.g., Mumbai)", "Mumbai")
num_pages = st.slider("Number of Pages to Scrape", 1, 5, 2)

if st.button("Fetch Jobs"):
    with st.spinner("Fetching job postings..."):
        naukri_jobs = scrape_naukri(job_title, location, num_pages)
        timesjobs_jobs = scrape_timesjobs(job_title, location, num_pages)

        # Combine both job lists
        all_jobs = naukri_jobs + timesjobs_jobs

        if all_jobs:
            df = pd.DataFrame(all_jobs)
            st.success(f"Fetched {len(all_jobs)} jobs!")
            st.dataframe(df)

            # Download option
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, "jobs.csv", "text/csv")
        else:
            st.warning("No jobs found. Try different keywords or location.")
