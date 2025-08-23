import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

# ---------------------------
# Scraper for Naukri
# ---------------------------
def scrape_naukri(job_title, location, num_pages=1):
    jobs = []
    for page in range(1, num_pages + 1):
        url = f"https://www.naukri.com/{job_title.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}-{page}"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        postings = soup.find_all("article", class_="jobTuple bgWhite br4 mb-8")
        
        for post in postings:
            title = post.find("a", class_="title").text.strip() if post.find("a", class_="title") else "N/A"
            company = post.find("a", class_="subTitle").text.strip() if post.find("a", class_="subTitle") else "N/A"
            loc_tag = post.find("li", class_="fleft grey-text br2 placeHolderLi location")
            location = loc_tag.text.strip() if loc_tag else "N/A"
            jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Source": "Naukri"
            })
    return jobs


# ---------------------------
# Scraper for TimesJobs
# ---------------------------
def scrape_timesjobs(job_title, location, num_pages=1):
    jobs = []
    for page in range(1, num_pages + 1):
        url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={job_title}&txtLocation={location}&sequence={page}&startPage=1"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        postings = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
        
        for post in postings:
            title = post.header.h2.a.text.strip() if post.header and post.header.h2 and post.header.h2.a else "N/A"
            company = post.find("h3", class_="joblist-comp-name").text.strip().split("\n")[0] if post.find("h3", class_="joblist-comp-name") else "N/A"
            
            # Fix: check if ul exists
            loc_tag = post.find("ul", class_="top-jd-dtl clearfix")
            location = loc_tag.li.text.strip() if loc_tag and loc_tag.li else "N/A"
            
            jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Source": "TimesJobs"
            })
    return jobs


# ---------------------------
# Streamlit Dashboard
# ---------------------------
st.title("Job Posting Aggregator")
st.write("Search for jobs across **Naukri** and **TimesJobs** 🚀")

job_title = st.text_input("Enter Job Title:", "Data Scientist")
location = st.text_input("Enter Location:", "Mumbai")
num_pages = st.slider("Number of Pages to Scrape", 1, 5, 1)

if st.button("Search Jobs"):
    st.write("🔎 Scraping jobs, please wait...")
    
    naukri_jobs = scrape_naukri(job_title, location, num_pages)
    timesjobs_jobs = scrape_timesjobs(job_title, location, num_pages)
    
    all_jobs = naukri_jobs + timesjobs_jobs
    df = pd.DataFrame(all_jobs)
    
    if not df.empty:
        st.success(f"✅ Found {len(df)} job postings!")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "jobs.csv", "text/csv")
    else:
        st.warning("⚠️ No jobs found. Try different keywords or location.")
