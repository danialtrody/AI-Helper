document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("sendBtn");
    const clearBtn = document.getElementById("clearBtn");
    const chatBox = document.getElementById("chat");
    const messageInput = document.getElementById("message");

    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        appendMessage("You", message);
        messageInput.value = "";

        try {
            let token = localStorage.getItem("token");
            let user_id = "guest";
            let username = "Guest";

            const headers = { "Content-Type": "application/json" };
            if (token) headers["Authorization"] = "Bearer " + token;

            const response = await fetch("/chat/", {
                method: "POST",
                headers: headers,
                body: JSON.stringify({
                    message,
                    user_id
                })
            });

            if (!response.ok) {
                const data = await response.json();
                appendMessage("System", `[Error] ${data.detail || "Failed to get reply"}`);
                return;
            }

            const data = await response.json();
            appendMessage("AI", data.reply);

        } catch (err) {
            appendMessage("System", "[Error] Could not get reply.");
            console.error(err);
        }
    }

    sendBtn.addEventListener("click", (e) => {
        e.preventDefault();
        sendMessage();
    });

    messageInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    clearBtn.addEventListener("click", (e) => {
        e.preventDefault();
        chatBox.innerHTML = "";
        messageInput.focus();
    });

    function appendMessage(sender, text) {
        const p = document.createElement("p");
        p.className = sender.toLowerCase().replace(/\s+/g, '-');
        p.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatBox.appendChild(p);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
