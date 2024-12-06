import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation

def load_data():
    with open('../data/wpi_courses.json', 'r', encoding='utf-8') as course_file:
        courses = json.load(course_file)

    with open('../data/adzunaAPI_jobs.json', 'r', encoding='utf-8') as jobs_file:
        jobs = json.load(jobs_file)

    return courses, jobs


def extract_dept_courses(courses, codes):
    descs = []
    for code in codes:
        descs += [course['Description'] for course in courses if course['Code'].startswith(code)]
    return descs

def extract_job_descriptions(jobs):
    job_descriptions = []
    for job in jobs:
        job_descriptions.append({
            'Title': job['Title'],
            'Description': job['Job Description'],
            'Employer': job['Employer'],
            'Location': job['Location'],
            'URL': job['URL']
        })
    return job_descriptions


def find_top_n_jobs_cosine(course_descriptions, job_descriptions, top_n=5):
    all_texts = course_descriptions + [job['Description'] for job in job_descriptions]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    course_vectors = tfidf_matrix[:len(course_descriptions)]
    job_vectors = tfidf_matrix[len(course_descriptions):]

    similarity_scores = cosine_similarity(course_vectors, job_vectors).mean(axis=0)

    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    top_jobs = [(job_descriptions[idx], similarity_scores[idx]) for idx in top_indices]

    return top_jobs


def find_top_n_jobs_lda(course_descriptions, job_descriptions, top_n=5, n_topics=10):
    all_texts = course_descriptions + [job['Description'] for job in job_descriptions]

    vectorizer = CountVectorizer(stop_words='english')
    count_matrix = vectorizer.fit_transform(all_texts)

    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda_matrix = lda.fit_transform(count_matrix)

    course_vectors = lda_matrix[:len(course_descriptions)]
    job_vectors = lda_matrix[len(course_descriptions):]

    similarity_scores = cosine_similarity(course_vectors, job_vectors).mean(axis=0)

    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    top_jobs = [(job_descriptions[idx], similarity_scores[idx]) for idx in top_indices]

    return top_jobs


def display_top_jobs(top_jobs):
    for idx, (job, score) in enumerate(top_jobs, start=1):
        print(f"\nRank {idx}:")
        print(f"Job Title: {job['Title']} at {job['Employer']}")
        print(f"Location: {job['Location']}")
        print(f"URL: {job['URL']}")
        print(f"Similarity Score: {score:.4f}")


def main():
    courses, jobs = load_data()

    course_codes = ['HI 1330', 'HI 2310', 'HI 2400', 'HI 3900', 'PY 1731', 'HI 2343', 'HI 2900', 'CS 3516',
                    'CS 2102', 'CS 1101', 'CS 2022', 'CS 2223', 'CS 3431', 'CS 3133', 'CS 3041', 'CS 3043',
                    'CS 2011', 'CS 4432', 'CS 4341', 'CS543', 'CS 502', 'CS 2303', 'MA 1021', 'MA 1022',
                    'MA 1023', 'MA 1024', 'MA 2051', 'MA 2611', 'MA 2631', 'PH 1110', 'PH 1121', 'BB 1002',
                    'BB 1035', 'CS 541', 'CS 547']
    course_descriptions = extract_dept_courses(courses, course_codes)
    job_descriptions = extract_job_descriptions(jobs)
    statistical = True
    top_n = 5

    if statistical:
        top_jobs = find_top_n_jobs_lda(course_descriptions, job_descriptions, top_n)
    else:
        top_jobs = find_top_n_jobs_cosine(course_descriptions, job_descriptions, top_n)

    display_top_jobs(top_jobs)


if __name__ == "__main__":
    main()
