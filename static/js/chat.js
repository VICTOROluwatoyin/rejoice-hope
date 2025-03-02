function addMessage(text, isUser) {
    const messages = document.getElementById("messages");
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${isUser ? "user" : "bot"}`;
    msgDiv.textContent = text;
    messages.appendChild(msgDiv);
    messages.scrollTop = messages.scrollHeight;
}

function sendChat() {
    const input = document.getElementById("input");
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, true); // Add user message
    input.value = "";          // Clear input

    fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            addMessage("Error: " + data.error, false);
        } else {
            addMessage(data.reply, false); // Add bot reply
        }
    })
    .catch(err => addMessage("Error: " + err.message, false));
}

// Send message on Enter (without Shift)
document.getElementById("input").addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendChat();
    }
});