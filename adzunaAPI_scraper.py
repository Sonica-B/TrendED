import requests
import pandas as pd
import os
import json

base_url = "https://api.adzuna.com/v1/api/jobs/us/search/"
APP_ID = "4772744a"
APP_KEY = "***REMOVED***"

def fetch(query, location, page):
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": query,
        "where": location,
        "results_per_page": 10,
    }

    url = f'{base_url}{page}'
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f"Retrieved page: {page} successfully")
        return response.json()
    else:
        print(f"Failed to retrieve data on page {page}: {response.status_code}")
        return None

def parse(data):
    jobs = []
    if "results" in data:
        print(data["results"])
        for job in data["results"]:
            # Store the required job data in the list
            jobs.append({
                "Title": job.get("title","N/A"),
                "Job Description": job.get("description","N/A"),
                "Employer": job.get("company","{}").get("display_name","N/A"),
                "Location": job.get("location","{}").get("display_name","N/A"),
                "URL": job.get("redirect_url","N/A"),
                "Minimum Salary": job.get("salary_min","N/A"),
                "Maximum Salary": job.get("salary_max","N/A"),
            })
    return jobs

def save_to_csv(data, file_path):
    if not data:
        print("No jobs to save.")
        return

    # Append to CSV if file exists, else create a new file with header
    jobs_df = pd.DataFrame(data)
    if os.path.isfile(file_path):
        jobs_df.to_csv(file_path, mode='a', index=False, header=False)
    else:
        jobs_df.to_csv(file_path, mode='w', index=False, header=True)

    print(f"Job listings saved to {file_path}")

def save_to_json(data, file_path):
    if not data:
        print("No jobs to save.")
        return

    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = [] # If file is empty or invalid, start with an empty list
    else:
        existing_data = []

    updated_data = existing_data + data

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, indent=4, ensure_ascii=False)

    print(f"Job listings saved to {file_path}")


def main():
    queries = ["Product Manager", "Business Analyst", "Technology Consultant"]
    location = "New York, NY"
    csv_file = "adzunaAPI_jobs.csv"
    json_file = "adzunaAPI_jobs.json"
    num_of_pages = 5

    job_listings = []

    for query in queries:
        print(f"Finding Job postings for: {query}")
        for page in range(1, num_of_pages+1):
            results = fetch(query,location,page)
            if results:
                jobs_data = parse(results)
                job_listings.extend(jobs_data)

    save_to_csv(job_listings, csv_file)
    save_to_json(job_listings, json_file)

if __name__ == "__main__":
    main()