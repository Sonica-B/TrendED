import json

from fastapi import APIRouter, Query

from utils.azure_blob_storage import container_client
from utils.comparator import TECHNICAL_SKILLS

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


@router.get("/get_skills")
async def get_skills():
    """Fetch all unique skills from WPI courses."""
    return TECHNICAL_SKILLS


@router.get("/get_courses")
async def get_courses(department: str = Query(...)):
    """Fetch courses for a specific department."""
    blob_client = container_client.get_blob_client("wpi_courses.json")
    try:
        course_data = json.loads(blob_client.download_blob().readall())
        filtered_courses = [
            {
                "code": course["Code"],
                "title": course["Title"],
                "description": course["Description"],
                "department": course["Department"],
            }
            for course in course_data
            if department == "All" or course["Department"] == department
        ]
        return filtered_courses
    except Exception as e:
        return {"error": str(e)}
