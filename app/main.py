from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import auth, comparator, course_scraper, job_scraper

app = FastAPI(title="TrendEd Pathfinder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Update the path to the actual static files location
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Include Routers
app.include_router(course_scraper.router, prefix="/courses", tags=["Course Scraping"])
app.include_router(job_scraper.router, prefix="/jobs", tags=["Job Matching"])
app.include_router(comparator.router, prefix="/compare", tags=["Comparison"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


@app.get("/")
async def root():
    return {"message": "Welcome to TrendEd Pathfinder API"}
