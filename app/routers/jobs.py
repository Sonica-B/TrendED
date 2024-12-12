import json

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from utils.azure_blob_storage import container_client
from utils.comparator import extract_job_descriptions, find_top_n_jobs_cosine

router = APIRouter()


@router.get("/find_jobs")
async def find_jobs(courses: str = Query(...), top_n: int = Query(5)):
    """Find top N jobs based on selected courses."""
    blob_client_courses = container_client.get_blob_client("wpi_courses.json")
    blob_client_jobs = container_client.get_blob_client("adzunaAPI_jobs.json")

    try:
        # Load courses and jobs from Azure Blob Storage
        course_data = json.loads(blob_client_courses.download_blob().readall())
        job_data = json.loads(blob_client_jobs.download_blob().readall())

        # Filter selected courses
        selected_course_codes = courses.split(",")
        selected_courses = [
            course for course in course_data if course["Code"] in selected_course_codes
        ]

        # Extract descriptions for matching
        course_descriptions = [course["Description"] for course in selected_courses]
        job_descriptions = extract_job_descriptions(job_data)

        # Perform comparison and find top jobs
        top_jobs = find_top_n_jobs_cosine(
            course_descriptions, job_descriptions, [1] * len(selected_courses), top_n
        )

        return [
            {
                "title": job[0]["Title"],
                "description": job[0]["Description"],
                "employer": job[0]["Employer"],
                "location": job[0]["Location"],
                "url": job[0]["URL"],
            }
            for job in top_jobs
        ]
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
