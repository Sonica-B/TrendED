from fastapi import APIRouter
from utils.comparator import *

router = APIRouter()


@router.get("/compare/")
async def comparator():
    main()

# async def compare_courses_jobs(dept_code: str, method: str = "cosine", top_n: int = 5):
#     courses, jobs = load_data()
#     course_descs = [course["Description"] for course in courses if course["Code"].startswith(dept_code)]
#     job_descs = [job for job in jobs]
#
#     if method == "cosine":
#         results = find_top_n_jobs_cosine(course_descs, job_descs, top_n)
#     elif method == "lda":
#         results = find_top_n_jobs_lda(course_descs, job_descs, top_n)
#     else:
#         return {"error": "Invalid method. Choose 'cosine' or 'lda'."}
#
#     return {"results": results}
