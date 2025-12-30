document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("sendBtn");
    const clearBtn = document.getElementById("clearBtn");
    const chatBox = document.getElementById("chat");
    const messageInput = document.getElementById("message");

    sendBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (!message) return;

        appendMessage("You", message);
        messageInput.value = "";

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message, user_id: "guest" })
            });
            const data = await response.json();
            appendMessage("AI", data.reply);
        } catch (err) {
            appendMessage("System", "[Error] Could not get reply.");
            console.error(err);
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
