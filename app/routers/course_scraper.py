from fastapi import APIRouter
from utils.azure_blob_storage import container_client
import json

router = APIRouter()

@router.get("/get_departments")
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
