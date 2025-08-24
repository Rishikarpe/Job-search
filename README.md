# Job Posting Aggregator

A **Streamlit-powered job aggregator** that scrapes job postings from **SimplyHired** and **TimesJobs**.  
It allows you to enter a job title, location, and number of pages, then displays results in an interactive table with an option to download the data as a CSV file. 🚀

---

## ✨ Features
- Scrapes jobs from:
  - ✅ SimplyHired
  - ✅ TimesJobs
- Extracts **title, company, location, summary, and job link**.
- Interactive **Streamlit UI**.
- Export results to **CSV** with one click.
- Lightweight and easy to customize.
<img width="662" height="576" alt="image" src="https://github.com/user-attachments/assets/a157e241-e532-46d1-8996-49e196446871" />


---


## ⚙️ Installation

1. Clone this repository or copy the files:
   ```bash
   git clone https://github.com/yourusername/job-aggregator.git
   cd job-aggregator

2. Install dependencies:
   ```bash
   pip install streamlit requests beautifulsoup4 pandas

3. Run the Streamlit app:
   ```bash
    streamlit run aggregator.py

## Example Output
| Title            | Company        | Location | Summary             | Link            | Source      |
| ---------------- | -------------- | -------- | ------------------- | --------------- | ----------- |
| Data Scientist   | Acme Corp      | Mumbai   | Work on ML models…  | simplyhired.com | SimplyHired |
| Python Developer | Tech Solutions | Pune     | Looking for Python… | timesjobs.com   | TimesJobs   |


## Output
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/aa55e62c-f4d9-4f31-8bab-f7b3b34e5285" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/ccb3eee0-a4b4-4857-a202-12e4f00c0f3b" />


