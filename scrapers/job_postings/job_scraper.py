import requests
import os
import json
from jobspy import scrape_jobs
from configs import *
from data.labels import QUERIES

# Dynamically set the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Define JSON file path relative to the project root
JSON_OUTPUT_FILE = os.path.join(PROJECT_ROOT, "data/json/jobs.json")

def fetch_adzuna_jobs(query, location, page):
    """
    Fetch jobs from Adzuna API.
    """
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": query,
        "where": location,
        "results_per_page": RESULTS_PER_PAGE,
    }
    url = f'{ADZUNA_BASE_URL}{page}'
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f"Adzuna - Retrieved page: {page} for query '{query}' successfully.")
        return response.json()
    else:
        print(f"Adzuna - Failed to retrieve data: {response.status_code}")
        return None

def parse_adzuna_results(data):
    """
    Parse results from Adzuna API.
    """
    jobs = []
    if "results" in data:
        for job in data["results"]:
            jobs.append({
                "Source": "Adzuna",
                "Title": job.get("title", "N/A"),
                "Job Description": job.get("description", "N/A"),
                "Employer": job.get("company", {}).get("display_name", "N/A"),
                "Location": job.get("location", {}).get("display_name", "N/A"),
                "URL": job.get("redirect_url", "N/A"),
            })
    return jobs


def fetch_jobspy_jobs(search_term, location):
    """
    Fetch jobs from JobSpy (e.g., Indeed, ZipRecruiter, Glassdoor, Google).
    """
    jobs = scrape_jobs(
        site_name=["indeed", "zip_recruiter", "glassdoor", "google"],
        search_term=search_term,
        google_search_term=f"{search_term} near {location}",
        location=location,
        results_wanted=RESULTS_WANTED,
        hours_old=HOURS_OLD,
        country_indeed=COUNTRY
    )
    print(f"JobSpy - Found {len(jobs)} jobs for query '{search_term}'.")
    return jobs

def parse_jobspy_results(jobs):
    """
    Parse results from JobSpy.
    """
    jobs_data = []
    if not jobs.empty:
        for _, row in jobs.iterrows():
            jobs_data.append({
                "Source": "JobSpy",
                "Title": row.get("title", "N/A"),
                "Job Description": row.get("description", "N/A"),
                "Employer": row.get("company", "N/A"),
                "Location": row.get("location", "N/A"),
                "URL": row.get("job_url", "N/A"),
            })
    return jobs_data

def save_to_json(data, file_path):
    """
    Save jobs to a JSON file.
    """
    # Ensure the directory for the output file exists
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)

    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    updated_data = existing_data + data

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, indent=4, ensure_ascii=False)

    print(f"Job listings saved to {file_path}")

def main():
    # Search Configuration
    course_code = input("Enter the Course Abbreviation (e.g., CS, DS): ").strip().upper()
    queries = QUERIES.get(course_code)
    location = "New York, NY"

    # Combined Job Listings
    all_jobs = []

    # Fetch and Parse Adzuna Jobs
    for query in queries:
        for page in range(1, NUM_OF_PAGES + 1):
            adzuna_results = fetch_adzuna_jobs(query, location, page)
            if adzuna_results:
                all_jobs.extend(parse_adzuna_results(adzuna_results))

    # Fetch and Parse JobSpy Jobs
    for query in queries:
        jobspy_results = fetch_jobspy_jobs(query, location)
        all_jobs.extend(parse_jobspy_results(jobspy_results))

    # Print total number of job postings retrieved
    print(f"Total number of job postings scraped: {len(all_jobs)}")

    # Save to JSON
    save_to_json(all_jobs, JSON_OUTPUT_FILE)

if __name__ == "__main__":
    main()