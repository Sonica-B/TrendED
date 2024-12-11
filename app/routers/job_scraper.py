import json
from fastapi import APIRouter, Query
from utils.adzunaAPI_scraper import fetch, parse, save_to_json
from utils.azure_blob_storage import upload_to_blob, container_client

router = APIRouter()

@router.get("/scrape_jobs/")
async def scrape_jobs(query: str = Query(...), location: str = Query(...), pages: int = 5):
    """
    Scrape jobs using Adzuna API based on the user's query and location.
    """
    all_jobs = []
    for page in range(1, pages + 1):
        # Fetch jobs from Adzuna API
        results = fetch(query, location, page)
        if results:
            jobs = parse(results)
            all_jobs.extend(jobs)

    # Save the results to a temporary JSON file
    local_file_path = "adzunaAPI_jobs.json"
    save_to_json(all_jobs, local_file_path)

    # Upload the JSON file to Azure Blob Storage, overwriting the existing file
    upload_to_blob(local_file_path, "adzunaAPI_jobs.json")

    return {"message": f"Scraped {len(all_jobs)} job postings and updated Azure Blob Storage."}

@router.get("/get_postings")
async def get_job_postings():
    """Fetch job postings from Azure Blob Storage."""
    blob_client = container_client.get_blob_client("adzunaAPI_jobs.json")
    try:
        job_data = blob_client.download_blob().readall()
        jobs = json.loads(job_data)
        return jobs
    except Exception as e:
        return {"error": str(e)}
