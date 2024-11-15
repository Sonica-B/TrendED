import requests
import pandas as pd
import os
import time

base_url = "https://api.adzuna.com/v1/api/jobs/us/search/"
APP_ID = "4772744a"
APP_KEY = "4b3246141e23b548d10c0dcc52789d3c"

def fetch(query, location, page):
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": query,
        "where": location,
        "results_per_page": 10,
    }

    url = f'{base_url}{page}'
    print(url)
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

    print(f"Files saved to {file_path}")

def main():
    query = "python developer"
    location = "boston"
    file_path = "adzunaAPI_jobs.csv"
    num_of_pages = 10

    job_listings = []

    for page in range(1, num_of_pages+1):
        results = fetch(query,location,page)
        if results:
            jobs_data = parse(results)
            job_listings.extend(jobs_data)

    save_to_csv(job_listings, file_path)

if __name__ == "__main__":
    main()