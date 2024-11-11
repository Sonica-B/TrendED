# TrendEd Pathfinder

## Project Overview
**TrendEd Pathfinder** is a tool designed to help students find internships and job opportunities that align with their skills and career goals. Through analyzing resumes, job postings, and identifying any skill gaps, TrendEd Pathfinder provides tailored job recommendations and suggests relevant courses for skill development.

### Team Members
- Shreya
- Sakshi
- Blake
- Harrison
- Ankit

---

## Purpose and Functionality

### Key Functions:
1. **Resume Analysis**: Extract key information (skills, education, experience) from a user’s resume.
2. **Job Matching**: Match resume content with relevant job postings.
3. **Skill Gap Identification**: Identify discrepancies between a candidate’s skills and the job requirements.
4. **Course Recommendations**: Suggest courses to fill identified skill gaps.

### Why This Tool?
Job search platforms typically offer only basic filtering options (by job type, category, company, etc.), often leading to a broad range of results that may not be the best fit. TrendEd Pathfinder seeks to provide a smarter, more personalized job search experience by considering the context of the individual user. Students and recent graduates seeking relevant internships and job opportunities would benefit from this tool’s refined recommendations.

### Differentiation
While some commercial solutions, like RippleMatch, offer similar services, TrendEd Pathfinder is designed to operate independently of job sources and does not require company participation. Unlike standard job-matching tools, it emphasizes **career development pathways** in addition to job matching.

### Challenges
The primary challenge is extracting and processing information from free-text job descriptions. This requires effective parsing to capture the relevant qualifications and requirements listed.

---

## Implementation Plan

### Data Collection
1. **Resume Input**: The user provides their resume, course details, and any additional relevant information.
2. **Course Catalog Scraping**: Web scraping of university course catalogs to gather information about skills and technologies covered in courses.
3. **Job Postings Scraping**: A separate web scraper will collect job descriptions from platforms like LinkedIn, Handshake, and Glassdoor. Future expansion may involve scraping company websites for additional context on company values and required skills.

### Core Algorithms and Techniques
- **Comparison Methods**: We are evaluating different approaches, including statistical language models, cosine similarity, and machine learning techniques, to match user skills with job requirements.
- **Libraries**:
  - BeautifulSoup for web scraping
  - scikit-learn or TensorFlow for machine learning algorithms
- **Development Environment**: Google Colab for managing code and handling computational tasks, especially for potential machine learning model development.

### Existing Resources
We aim to leverage existing scraping and parsing tools where available, as well as well-established ML libraries for efficient algorithm development.

---

## Demonstration and Evaluation

### Testing
Our team, being students actively engaged in the job search process, will utilize TrendEd Pathfinder to ensure its functionality and accuracy. Additionally, we’ll invite fellow students to try the tool, gathering feedback and refining the model based on user surveys.

## Branching Strategy

![Image](https://github.com/user-attachments/assets/7df4e810-02ff-4304-9905-8a6b1745bf5a)


### 1. Main Branches
- **main branch:** This is the stable branch with production-ready code. Only thoroughly reviewed and tested code is merged here.
- **integration branch:** This branch is for integrating features before they’re finalized. All new features and bug fixes are merged into this branch first. Regularly updated from team members' contributions, it serves as the main staging area.

### 2. Development Branches
- **Feature branches (feature/branch-name):** Each team member should create a feature branch off `integration`for a specific task or feature. These branches focus on specific parts of the project (e.g., `feature/data-preprocessing`, `feature/model-selection`, etc.). Each `feature branch` is merged back into `integration`once complete.
- Naming Convention:  ` feature/short-description`  (e.g., `feature/data-collection`, `feature/model-training`)

- **Bugfix branches (bugfix/branch-name):** If issues arise during development, team members can create branches off `integration`for bug fixes. These branches are named descriptively (e.g., `bugfix/data-cleaning-issue`) and merged back into `integration`after testing.
- Naming Convention:  `bugfix/short-description` (e.g., `bugfix/missing-values`, `bugfix/model-overfitting`)

### 3. Pull Requests:
When ready, team members open Pull Requests (PRs) from feature branches into integration, moving the linked task in GitHub Projects to Review.
Other team members review the PR and suggest improvements if needed. Once approved, merge it into `integration`.

## Workflow
Planning and Assignment: Break down the project into distinct tasks (e.g., data preprocessing, feature engineering, model training, evaluation). Ensure that everyone has a clear feature branch in which to work.

**Daily Development:**
- Each team member pulls the latest integration branch and works on their respective feature branches.
- Team members commit frequently and push updates to their feature branches.

**Regular Integration:**
- Designate short integration sessions (e.g., every 2-3 days) for all members to merge their feature branches into integration.
- Review each feature branch with code reviews to check for any conflicts or issues.

 **Testing and Finalizing:**
- Toward the end of the project, focus on integrating and thoroughly testing the code in integration.
- Conduct final testing and review on the `integration` branch, and then merge it into `main `once the project reaches a stable, production-ready state.


## Final Wrap-Up
When the project is complete and ready to submit, ensure all code from `integration` is thoroughly tested and merged into `main` for the final version. Tag this final commit as **v1.0.**




---

By creating TrendEd Pathfinder, we aim to provide students with a more targeted and supportive job search experience, helping them to find meaningful career opportunities and providing recommendations for continuous skill development.
