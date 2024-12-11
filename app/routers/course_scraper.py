from fastapi import APIRouter
from utils.WPI_course_scraper import *

router = APIRouter()

@router.get("/scrape_courses/")
async def scrape_courses():
    main()  # Assuming main() from WPI_course_scraper handles scraping
    return {"message": "Courses scraped successfully."}
