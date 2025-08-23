import streamlit as st
import pandas as pd
import subprocess
import os

# --- Function to run scraper ---
async def run_scraper(job_title, location):
    # Run your existing scraper script
    process = subprocess.run(
        ["python", "steam.py", job_title, location], capture_output=True, text=True
    )
    st.text(process.stdout)
    st.text(process.stderr)

# --- Streamlit App ---
st.set_page_config(page_title="Job Aggregator", layout="wide")

st.title("📊 Job Posting Aggregator (Naukri.com)")

# Inputs
job_title = st.text_input("Job Title", "Python Developer")
location = st.text_input("Location", "Mumbai")

if st.button("Scrape Jobs"):
    with st.spinner("Scraping jobs..."):
        # Call scraper (runs steam.py with params)
        os.system(f"python steam.py \"{job_title}\" \"{location}\"")

# Show results if CSV exists
if os.path.exists("jobs.csv"):
    df = pd.read_csv("jobs.csv")
    st.success(f"✅ Loaded {len(df)} jobs")
    st.dataframe(df)

    # Download option
    st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), "jobs.csv", "text/csv")