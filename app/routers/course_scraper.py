from fastapi import APIRouter, Query
from utils.azure_blob_storage import container_client
import json

router = APIRouter()

@router.get("/get_departments")
async def get_departments():
    """Fetch all unique departments from WPI courses."""
    blob_client = container_client.get_blob_client("wpi_courses.json")
    try:
        course_data = json.loads(blob_client.download_blob().readall())
        departments = list(set(course["Department"] for course in course_data))
        return departments
    except Exception as e:
        return {"error": str(e)}

@router.get("/get_courses")
async def get_courses(department: str = Query(...)):
    """Fetch courses for a specific department."""
    blob_client = container_client.get_blob_client("wpi_courses.json")
    try:
        course_data = json.loads(blob_client.download_blob().readall())
        filtered_courses = [
            {"Code": course["Code"], "Title": course["Title"], "Description": course["Description"]}
            for course in course_data if course["Department"] == department
        ]
        return filtered_courses
    except Exception as e:
        return {"error": str(e)}
