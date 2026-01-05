document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");

    if (!registerForm) {
        console.error("Register form not found in DOM.");
        return;
    }

    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();
        const confirmPassword = document.getElementById("confirmPassword").value.trim();

        if (!username || !password || !confirmPassword) {
            alert("Please fill in all fields.");
            return;
        }

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        try {
            const response = await fetch("/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                const data = await response.json();
                alert(data.detail || "Registration failed");
                return;
            }

            const data = await response.json();
            console.log("Registration success:", data);

            alert("Registration successful! Redirecting to login...");
            window.location.href = "/login-page";
        } catch (err) {
            console.error("Registration error:", err);
            alert("An error occurred. Please try again.");
        }
    });
});
