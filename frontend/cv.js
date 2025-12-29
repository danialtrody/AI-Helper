document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.getElementById("submitBtn");
    const clearBtn = document.getElementById("clearBtn");
    const feedbackBox = document.getElementById("feedback");
    const jobTitleInput = document.getElementById("jobTitle");
    const cvFileInput = document.getElementById("cvFile");

    submitBtn.addEventListener("click", async (e) => {
        e.preventDefault();

        const jobTitle = jobTitleInput.value.trim();
        const file = cvFileInput.files[0];

        if (!jobTitle || !file) {
            appendMessage("System", "Please enter a job title and select a CV file.");
            return;
        }

        appendMessage("System", `Uploading CV: ${file.name}...`);

        try {
            const formData = new FormData();
            formData.append("file", file);
            formData.append("job_title", jobTitle);
            formData.append("user_id", "guest");

            const response = await fetch("/cv/upload", {  // <-- תואם ל-backend
                method: "POST",
                body: formData
            });

            const data = await response.json();
            appendMessage("AI Feedback", data.feedback);

        } catch (err) {
            appendMessage("System", "[Error] Could not get feedback.");
            console.error(err);
        }
    });

    clearBtn.addEventListener("click", (e) => {
        e.preventDefault();
        feedbackBox.innerHTML = "";
        jobTitleInput.value = "";
        cvFileInput.value = "";
        jobTitleInput.focus();
    });

    function appendMessage(sender, text) {
        const p = document.createElement("p");
        p.className = sender.toLowerCase().replace(/\s+/g, '-');
        p.innerHTML = `<strong>${sender}:</strong> ${text}`;
        feedbackBox.appendChild(p);
        feedbackBox.scrollTop = feedbackBox.scrollHeight;
    }
});
