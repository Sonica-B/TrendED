import json
from fastapi import APIRouter, Query
from utils.azure_blob_storage import container_client
from utils.comparator import extract_dept_courses, extract_job_descriptions, find_top_n_jobs_cosine

router = APIRouter()

@router.get("/courses/get_departments")
async def get_departments():
    """Fetch all unique departments from WPI courses."""
    blob_client = container_client.get_blob_client("wpi_courses.json")
    try:
        course_data = blob_client.download_blob().readall()
        courses = json.loads(course_data)
        departments = list(set(course["Department"] for course in courses))
        return departments
    except Exception as e:
        return {"error": str(e)}

@router.get("/courses/get_courses")
async def get_courses(department: str = Query(...)):
    """Fetch courses for a specific department."""
    blob_client = container_client.get_blob_client("wpi_courses.json")
    try:
        course_data = blob_client.download_blob().readall()
        courses = json.loads(course_data)
        filtered_courses = [course for course in courses if course["Department"] == department]
        return filtered_courses
    except Exception as e:
        return {"error": str(e)}

@router.get("/jobs/find_jobs")
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
        selected_courses = [course for course in course_data if course["Code"] in selected_course_codes]

        # Perform comparison
        course_descriptions = [course["Description"] for course in selected_courses]
        job_descriptions = extract_job_descriptions(job_data)
        top_jobs = find_top_n_jobs_cosine(course_descriptions, job_descriptions, top_n)

        return [job[0] for job in top_jobs]
    except Exception as e:
        return {"error": str(e)}

