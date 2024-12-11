from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import courses, jobs, user

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
app.include_router(courses.router, prefix="/courses", tags=["Course Api"])
app.include_router(jobs.router, prefix="/jobs", tags=["Job Api"])
app.include_router(user.router, prefix="/user", tags=["User Api"])


# Update the path to the actual static files location
app.mount("/", StaticFiles(directory="dist", html=True))


@app.api_route("/{path_name:path}", methods=["GET"])
async def catch_all():
    return FileResponse("dist/index.html")
