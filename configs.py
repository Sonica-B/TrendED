# File Paths
COURSES_FILES = "data/json/wpi_courses.json"  # Update with your file path
JOB_FILES = "data/json/jobs.json"  # Update with your file path
SIMILARITY_FILE = "data/json/similarity_results.json"

"""
    Job Scraper parameters used by AdzunaAPI.
"""
ADZUNA_APP_ID = "4772744a"
ADZUNA_APP_KEY = "4b3246141e23b548d10c0dcc52789d3c"
ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/"
RESULTS_PER_PAGE = 10
NUM_OF_PAGES = 5

"""
    Job Scraper parameters used by JobSpy Library.
"""
RESULTS_WANTED = 100
HOURS_OLD = 72
COUNTRY = "USA"