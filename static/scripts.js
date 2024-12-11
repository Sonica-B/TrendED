// Populate departments on page load
document.addEventListener("DOMContentLoaded", async () => {
    try {
        // Fetch departments from Azure Blob
        const response = await fetch("/courses/get_departments");
        if (!response.ok) {
            throw new Error("Failed to fetch departments.");
        }
        const departments = await response.json();

        // Populate department dropdown
        const departmentSelect = document.getElementById("departments");
        departments.forEach((dept) => {
            const option = document.createElement("option");
            option.value = dept;
            option.textContent = dept;
            departmentSelect.appendChild(option);
        });

        // Add change event listener to load courses for selected department
        departmentSelect.addEventListener("change", async () => {
            const selectedDept = departmentSelect.value;
            await loadCourses(selectedDept);
        });
    } catch (error) {
        console.error("Error fetching departments:", error.message);
    }
});

// Load courses based on selected department
async function loadCourses(department) {
    try {
        const response = await fetch(`/courses/get_courses?department=${department}`);
        if (!response.ok) {
            throw new Error("Failed to fetch courses.");
        }
        const courses = await response.json();

        // Populate courses dropdown
        const courseSelect = document.getElementById("courses");
        courseSelect.innerHTML = ""; // Clear existing options
        courses.forEach((course) => {
            const option = document.createElement("option");
            option.value = course.Code;
            option.textContent = `${course.Code} - ${course.Title}`;
            courseSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching courses:", error.message);
    }
}

// Handle form submission
document.getElementById("course-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const selectedCourses = Array.from(document.getElementById("courses").selectedOptions).map(
        (option) => option.value
    );
    const topN = document.getElementById("top-n").value;

    try {
        // Fetch top job postings based on selected courses
        const response = await fetch(`/jobs/find_jobs?courses=${selectedCourses.join(",")}&top_n=${topN}`);
        if (!response.ok) {
            throw new Error("Failed to fetch job postings.");
        }
        const jobs = await response.json();

        displayJobPostings(jobs);
    } catch (error) {
        document.getElementById("job-results").innerHTML = `<p>Error: ${error.message}</p>`;
    }
});

function displayJobPostings(jobs) {
    const jobResults = document.getElementById("job-results");
    jobResults.innerHTML = ""; // Clear existing content

    if (jobs.length === 0) {
        jobResults.innerHTML = "<p>No job postings found.</p>";
        return;
    }

    jobs.forEach((job) => {
        const jobCard = document.createElement("div");
        jobCard.className = "job-card";
        jobCard.innerHTML = `
            <h3>${job.Title}</h3>
            <p><strong>Company:</strong> ${job.Employer}</p>
            <p><strong>Location:</strong> ${job.Location}</p>
            <p>${job["Job Description"]}</p>
            <a href="${job.URL}" target="_blank" class="apply-button">Apply Now</a>
        `;
        jobResults.appendChild(jobCard);
    });
}