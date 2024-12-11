import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation

# Define technical skills
TECHNICAL_SKILLS = [
    # Programming
    "Python", "Java", "C++", "R", "MATLAB",
    # Artificial Intelligence
    "Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision",
    # Data Analysis
    "Big Data", "Data Mining", "Data Visualization", "Statistical Modeling",
    # Cloud & Web
    "Cloud Computing", "AWS", "Azure", "Web Development", "API Integration",
    # Cybersecurity
    "Cryptography", "Network Security", "Ethical Hacking",
    # Engineering
    "Structural Analysis", "Thermodynamics", "Fluid Dynamics", "CAD", "CAM", "FEA",
    # Life Sciences
    "Genomics", "Proteomics", "Bioinformatics", "Clinical Research", "Biomedical Imaging",
    # Robotics & Control
    "Embedded Systems", "IoT", "Autonomous Systems", "Robot Kinematics", "Dynamics",
    # Simulation & Modeling
    "Simulink", "Finite Element Analysis", "Agent-Based Modeling",
    # Data Management
    "SQL", "NoSQL Databases", "Data Warehousing",
    # Software Development
    "Agile", "Scrum", "Version Control", "Microservices",
    # Electrical & Electronics
    "Circuit Design", "FPGA", "Power Systems", "Signal Processing",
    # Sustainable Engineering
    "Renewable Energy Systems", "Sustainable Design", "Environmental Impact Assessment",
    # Networking
    "Wireless Communication", "Network Design", "Telecommunications",
    # Non-Technical Skills
    "Technical Writing", "Public Speaking", "Cross-Cultural Communication",
    "Budgeting", "Risk Management", "Team Leadership", "Literature Review",
    "Experimental Design", "Data Interpretation", "Analytical Thinking",
    "Critical Thinking", "Creative Problem-Solving", "Architectural Design",
    "User Experience Design", "Interface Design", "Business Analysis",
    "Market Research", "Product Strategy", "Curriculum Development",
    "Mentoring", "Educational Technology"
]

def load_data():
    with open('../data/json/wpi_courses.json', 'r', encoding='utf-8') as course_file:
        courses = json.load(course_file)

    with open('../data/json/jobs.json', 'r', encoding='utf-8') as jobs_file:
        jobs = json.load(jobs_file)

    return courses, jobs


def extract_dept_courses(courses, codes):
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
            else:
                 print(f"Dupe code '{code}'")

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

def generate_skills_vector(skills):
    """
    Generate a vector representation of technical skills using SentenceTransformer.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    skills_text = " ".join(skills)
    return model.encode(skills_text)

def combine_descriptions_with_skills(course_descriptions, skills):
    """
    Combine course descriptions with the technical skills as text.
    """
    combined_descriptions = [
        f"{desc} {' '.join(skills)}"
        for desc in course_descriptions
    ]
    return combined_descriptions

def find_top_n_jobs_cosine(course_descriptions, job_descriptions, course_weights, top_n=5):
    all_texts = course_descriptions + [job['Description'] for job in job_descriptions]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    course_vectors = tfidf_matrix[:len(course_descriptions)]
    job_vectors = tfidf_matrix[len(course_descriptions):]

    course_weights = np.array(course_weights).reshape(-1, 1)
    weighted_course_vectors = course_vectors * course_weights

    similarity_scores = cosine_similarity(weighted_course_vectors, job_vectors).mean(axis=0)

    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    top_jobs = [(job_descriptions[idx], similarity_scores[idx]) for idx in top_indices]

    return top_jobs


def find_top_n_jobs_lda(course_descriptions, job_descriptions, course_weights, top_n=5, n_topics=10):
    all_texts = course_descriptions + [job['Description'] for job in job_descriptions]
    vectorizer = CountVectorizer(stop_words='english')
    count_matrix = vectorizer.fit_transform(all_texts)

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


def display_top_jobs(top_jobs):
    for idx, (job, score) in enumerate(top_jobs, start=1):
        print(f"\nRank {idx}:")
        print(f"Job Title: {job['Title']} at {job['Employer']}")
        print(f"Location: {job['Location']}")
        print(f"URL: {job['URL']}")
        print(f"Similarity Score: {score:.4f}")


def main():
    # Load course and job data
    courses, jobs = load_data()

    # Define course codes and weights
    course_codes = ['HI 1330', 'HI 2310', 'HI 2400', 'PY 1731', 'HI 2343', 'HI 2900', 'CS 3516',
                    'CS 2102', 'CS 1101', 'CS 2022', 'CS 2223', 'CS 3431', 'CS 3133', 'CS 3041', 'CS 3043',
                    'CS 2011', 'CS 4432', 'CS 4341', 'CS 543', 'CS 502', 'CS 2303', 'MA 1021', 'MA 1022',
                    'MA 1023', 'MA 1024', 'MA 2051', 'MA 2611', 'MA 2631', 'PH 1110', 'PH 1121', 'BB 1002',
                    'BB 1035', 'CS 541', 'CS 547']  # Example
    course_weights = [1 if code.startswith('CS') else 0 for code in course_codes if code in {course['Code'] for course in courses}]

    # Extract course and job descriptions
    course_descriptions = extract_dept_courses(courses, course_codes)
    job_descriptions = extract_job_descriptions(jobs)

    # Combine course descriptions with skills as text
    combined_descriptions = combine_descriptions_with_skills(course_descriptions, TECHNICAL_SKILLS)

    # Choose similarity method
    statistical = True
    top_n = 5

    if statistical:
        # Pass combined text descriptions to the LDA-based method
        top_jobs = find_top_n_jobs_lda(combined_descriptions, job_descriptions, course_weights, top_n)
    else:
        # For cosine similarity, generate embeddings
        model = SentenceTransformer('all-MiniLM-L6-v2')
        course_vectors = model.encode(combined_descriptions)
        top_jobs = find_top_n_jobs_cosine(course_vectors, job_descriptions, course_weights, top_n)

    # Display the results
    display_top_jobs(top_jobs)

if __name__ == "__main__":
    main()

