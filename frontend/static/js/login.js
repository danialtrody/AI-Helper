document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const loginError = document.getElementById("loginError");

    if (!loginForm || !loginError) {
        console.error("Login form or error element not found in DOM.");
        return;
    }

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        loginError.textContent = "";

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!username || !password) {
            loginError.textContent = "Please enter both username and password.";
            return;
        }

        try {
            const response = await fetch("/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({ username, password })
            });

            if (!response.ok) {
                const data = await response.json();
                loginError.textContent = data.detail || "Login failed";
                return;
            }

            const data = await response.json();
            console.log("Login success:", data);

            localStorage.setItem("token", data.access_token);

            window.location.href = "/chat";
        } catch (err) {
            console.error(err);
            loginError.textContent = "An error occurred. Please try again.";
        }
    });
});
