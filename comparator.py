import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation

TECHNICAL_SKILLS = [
    # Programming Languages and Tools
    "Python", "Java", "C++", "R", "MATLAB", "Simulink", "SQL", "NoSQL", "HTML", "CSS", "JavaScript",
    # Artificial Intelligence and Data Science
    "Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision", "Big Data",
    "Data Analysis", "Data Mining", "Data Visualization", "Statistical Modeling", "Predictive Analytics",
    # Cloud and Web Development
    "Cloud Computing", "AWS", "Azure", "GCP", "Web Development", "API Integration",
    # Cybersecurity
    "Cryptography", "Network Security", "Ethical Hacking", "Incident Response", "Security Audits",
    # Engineering and Robotics
    "Structural Analysis", "Thermodynamics", "Fluid Dynamics", "Finite Element Analysis", "CAD", "CAM",
    "Embedded Systems", "IoT", "Autonomous Systems", "Robot Kinematics", "Dynamics",
    # Biomedical and Life Sciences
    "Genomics", "Proteomics", "Bioinformatics", "Clinical Research", "Biomedical Imaging",
    # Software Development and Agile
    "Agile Development", "Scrum", "Version Control", "Git", "Microservices", "DevOps",
    # Electrical and Electronics
    "Circuit Design", "FPGA", "Power Systems", "Signal Processing", "Wireless Communication",
    # Sustainability and Renewable Energy
    "Renewable Energy Systems", "Sustainable Design", "Environmental Impact Assessment",
    # Project Management and Communication
    "Technical Writing", "Public Speaking", "Team Leadership", "Risk Management", "Budgeting",
    # Research and Problem Solving
    "Experimental Design", "Literature Review", "Data Interpretation", "Analytical Thinking",
    "Creative Problem Solving", "Critical Thinking",
    # Design and User Experience
    "Architectural Design", "User Experience Design", "Interface Design", "Prototyping",
    # Strategic Planning and Business Skills
    "Business Analysis", "Market Research", "Product Strategy", "Entrepreneurship",
    # Education and Mentorship
    "Curriculum Development", "Mentoring", "Educational Technology"
]

def load_data():
    with open('../data/json/wpi_courses.json', 'r', encoding='utf-8') as course_file:
        courses = json.load(course_file)

    with open('../data/json/jobs.json', 'r', encoding='utf-8') as jobs_file:
        jobs = json.load(jobs_file)

    return courses, jobs

def deduplicate_jobs(jobs):
    """
    Deduplicate jobs based on Title, Employer, and Location.
    """
    seen = set()
    unique_jobs = []
    for job in jobs:
        job_id = (job['Title'], job['Employer'], job['Location'])
        if job_id not in seen:
            seen.add(job_id)
            unique_jobs.append(job)
    return unique_jobs

def extract_dept_courses(courses, codes):
    """
    Extract unique course descriptions based on course codes.
    """
    descs = []
    added_descriptions = set()

    for code in codes:
        matched_courses = [course['Description'] for course in courses if course['Code'].startswith(code)]

        if not matched_courses:
            print(f"No course for code '{code}'.")

        for course in matched_courses:
            if course not in added_descriptions:
                descs.append(course)
                added_descriptions.add(course)

    return descs

def extract_job_descriptions(jobs):
    """
    Extract relevant job descriptions containing at least one technical skill.
    """
    jobs = deduplicate_jobs(jobs)
    job_descriptions = []
    for job in jobs:
        if any(skill.lower() in job['Job Description'].lower() for skill in TECHNICAL_SKILLS):
            job_descriptions.append({
                'Title': job['Title'],
                'Description': job['Job Description'],
                'Employer': job['Employer'],
                'Location': job['Location'],
                'URL': job['URL']
            })
    return job_descriptions

def find_top_n_jobs_cosine(course_descriptions, job_descriptions, course_weights, top_n=5):
    """
    Find top N jobs using cosine similarity with TF-IDF vectors.
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(course_descriptions + [job['Description'] for job in job_descriptions])

    course_vectors = tfidf_matrix[:len(course_descriptions)]
    job_vectors = tfidf_matrix[len(course_descriptions):]

    course_weights = np.array(course_weights).reshape(-1, 1)
    weighted_course_vectors = course_vectors.multiply(course_weights)

    similarity_scores = cosine_similarity(weighted_course_vectors, job_vectors).mean(axis=0)

    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    top_jobs = [(job_descriptions[idx], similarity_scores[idx]) for idx in top_indices]

    return top_jobs

def find_top_n_jobs_lda(course_descriptions, job_descriptions, course_weights, top_n=5, n_topics=5):
    """
    Find top N jobs using Latent Dirichlet Allocation (LDA).
    """
    vectorizer = CountVectorizer(stop_words='english')
    count_matrix = vectorizer.fit_transform(course_descriptions + [job['Description'] for job in job_descriptions])

    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda_matrix = lda.fit_transform(count_matrix)

    course_vectors = lda_matrix[:len(course_descriptions)]
    job_vectors = lda_matrix[len(course_descriptions):]

    course_weights = np.array(course_weights).reshape(-1, 1)
    weighted_course_vectors = course_vectors * course_weights

    similarity_scores = cosine_similarity(weighted_course_vectors, job_vectors).mean(axis=0)

    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    top_jobs = [(job_descriptions[idx], similarity_scores[idx]) for idx in top_indices]

    return top_jobs

def calculate_evaluation_metrics(top_jobs, job_descriptions, ground_truth=None):
    """
    Calculate evaluation metrics for the top jobs.
    """
    scores = [score for _, score in top_jobs]
    mean_score = np.mean(scores)
    std_dev = np.std(scores)

    unique_titles = len(set(job['Title'] for job, _ in top_jobs))
    unique_employers = len(set(job['Employer'] for job, _ in top_jobs))

    # Precision at K (P@K)
    precision_at_k = len(top_jobs) / len(job_descriptions) if len(job_descriptions) > 0 else 0

    # Discounted Cumulative Gain (DCG)
    dcg = sum((2 ** score - 1) / np.log2(idx + 2) for idx, (_, score) in enumerate(top_jobs))

    # Normalized Discounted Cumulative Gain (nDCG)
    idcg = sum((2 ** score - 1) / np.log2(idx + 2) for idx, score in enumerate(sorted(scores, reverse=True)))
    ndcg = dcg / idcg if idcg > 0 else 0

    # Redundancy Check
    redundancy = 1 - (unique_titles / len(top_jobs))

    return {
        "Mean Similarity Score": round(mean_score, 4),
        "Standard Deviation of Scores": round(std_dev, 4),
        "Job Title Diversity": round(unique_titles / len(top_jobs), 4),
        "Employer Diversity": round(unique_employers / len(top_jobs), 4),
        "Precision at K": round(precision_at_k, 4),
        "Discounted Cumulative Gain (DCG)": round(dcg, 4),
        "Normalized DCG (nDCG)": round(ndcg, 4),
        "Redundancy": round(redundancy, 4)
    }

def display_top_jobs(top_jobs):
    """
    Display the top jobs.
    """
    for idx, (job, score) in enumerate(top_jobs, start=1):
        print(f"\nRank {idx}:")
        print(f"Job Title: {job['Title']} at {job['Employer']}")
        print(f"Location: {job['Location']}")
        print(f"URL: {job['URL']}")
        print(f"Similarity Score: {score:.4f}")

def save_top_jobs_to_json(top_jobs):
    jobs = []
    for idx, (job, score) in enumerate(top_jobs, start=1):
        jobs.append({
            "Rank": idx,
            "Job Title": f"{job['Title']} at {job['Employer']}",
            "Location": job['Location'],
            "URL": job['URL'],
            "Similarity Score": round(float(score), 4)
        })

    with open('../data/json/top_jobs.json', 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)

def main():
    # Load course and job data
    courses, jobs = load_data()

    # Define course codes and weights
    course_codes = ['CS 3516', 'CS 2102', 'CS 1101', 'CS 2022', 'CS 2223']  # Example
    course_weights = [1 if code.startswith('CS') else 0 for code in course_codes if code in {course['Code'] for course in courses}]

    # Extract course and job descriptions
    course_descriptions = extract_dept_courses(courses, course_codes)
    job_descriptions = extract_job_descriptions(jobs)

    # Choose similarity method
    statistical = True
    top_n = 20

    if statistical:
        top_jobs = find_top_n_jobs_lda(course_descriptions, job_descriptions, course_weights, top_n)
    else:
        top_jobs = find_top_n_jobs_cosine(course_descriptions, job_descriptions, course_weights, top_n)

    # Display the results
    display_top_jobs(top_jobs)
    save_top_jobs_to_json(top_jobs)

    # Calculate and display evaluation metrics
    evaluation_metrics = calculate_evaluation_metrics(top_jobs, job_descriptions)
    print("\nEvaluation Metrics:")
    for metric, value in evaluation_metrics.items():
        print(f"{metric}: {value}")

if __name__ == "__main__":
    main()
