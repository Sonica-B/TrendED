from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import job_scraper, course_scraper, comparator

app = FastAPI(title="TrendEd Pathfinder API")

# Update the path to the actual static files location
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Include Routers
app.include_router(course_scraper.router, prefix="/courses", tags=["Course Scraping"])
app.include_router(job_scraper.router, prefix="/jobs", tags=["Job Matching"])
app.include_router(comparator.router, prefix="/compare", tags=["Comparison"])




@app.get("/")
async def root():
    return {"message": "Welcome to TrendEd Pathfinder API"}


