document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("/courses/get_departments");
        if (!response.ok) {
            throw new Error("Failed to fetch departments.");
        }
        const departments = await response.json();

        const departmentSelect = document.getElementById("departments");
        departments.forEach((dept) => {
            const option = document.createElement("option");
            option.value = dept;
            option.textContent = dept;
            departmentSelect.appendChild(option);
        });

        departmentSelect.addEventListener("change", async () => {
            const selectedDept = departmentSelect.value;
            await loadCourses(selectedDept);
        });
    } catch (error) {
        console.error("Error fetching departments:", error.message);
    }
});

async function loadCourses(department) {
    try {
        const response = await fetch(`/courses/get_courses?department=${department}`);
        if (!response.ok) {
            throw new Error("Failed to fetch courses.");
        }
        const courses = await response.json();

        const courseList = document.getElementById("course-list");
        courseList.innerHTML = ""; // Clear existing content
        courses.forEach((course) => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `
                <input type="checkbox" value="${course.Code}" id="${course.Code}">
                <label for="${course.Code}">${course.Code} - ${course.Title}</label>
            `;
            courseList.appendChild(listItem);
        });
    } catch (error) {
        console.error("Error fetching courses:", error.message);
    }
}

document.getElementById("course-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const selectedCourses = Array.from(document.querySelectorAll("#course-list input[type='checkbox']:checked"))
        .map((checkbox) => checkbox.value);
    const topN = document.getElementById("top-n").value;

    try {
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
    jobResults.innerHTML = "";

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
