document.getElementById("job-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = document.getElementById("query").value;
    const location = document.getElementById("location").value;

    try {
        // Step 1: Trigger the scraping process
        const scrapeResponse = await fetch(`/jobs/scrape_jobs/?query=${query}&location=${location}`);
        if (!scrapeResponse.ok) {
            throw new Error('Failed to scrape job postings.');
        }
        const scrapeResult = await scrapeResponse.json();
        console.log(scrapeResult.message); // Debugging message to verify scraping

        // Step 2: Fetch updated job postings
        const response = await fetch(`/jobs/get_postings`);
        if (!response.ok) {
            throw new Error('Failed to fetch updated job postings.');
        }
        const data = await response.json();

        if (!Array.isArray(data)) {
            throw new Error('Unexpected response format. Expected an array of jobs.');
        }

        displayJobPostings(data); // Display updated job postings
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
