document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("sendBtn");
    const messageInput = document.getElementById("message");
    const chatBox = document.getElementById("chat");
    const clearBtn = document.getElementById("clearBtn");

    sendBtn.addEventListener("click", (e) => {
        e.preventDefault();
        sendMessage();
    });

    clearBtn.addEventListener("click", (e) => {
        e.preventDefault();  // Prevent default
        chatBox.innerHTML = "";
        messageInput.value = "";
        messageInput.focus();
    });

    messageInput.addEventListener("keypress", function(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        appendMessage("You", message);

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            appendMessage("AI", data.reply);
        } catch (err) {
            appendMessage("AI", "[Error] Could not get response");
            console.error(err);
        }

        messageInput.value = "";
        messageInput.focus();
    }

    function appendMessage(sender, text) {
        const p = document.createElement("p");
        p.className = sender.toLowerCase();
        p.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatBox.appendChild(p);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
