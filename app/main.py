from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import auth, comparator, course_scraper, job_scraper

app = FastAPI(title="TrendEd Pathfinder API")

# for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(course_scraper.router, prefix="/courses", tags=["Course Scraping"])
app.include_router(job_scraper.router, prefix="/jobs", tags=["Job Matching"])
app.include_router(comparator.router, prefix="/compare", tags=["Comparison"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


# Update the path to the actual static files location
app.mount("/", StaticFiles(directory="dist", html=True))


@app.api_route("/{path_name:path}", methods=["GET"])
async def catch_all():
    return FileResponse("dist/index.html")
