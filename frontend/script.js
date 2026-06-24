const statusEl = document.getElementById("status");
const button = document.getElementById("markReadBtn");

button.addEventListener("click", async () => {
    statusEl.textContent = "Marking unread emails as read...";
    button.disabled = true;

    try {
        const response = await fetch("/api/mark-read", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        });

        const data = await response.json();
        if (data.success) {
            statusEl.textContent = data.message;
        } else {
            statusEl.textContent = "Failed to mark emails as read.";
        }
    } catch (error) {
        console.error(error);
        statusEl.textContent = "Error connecting to backend.";
    } finally {
        button.disabled = false;
    }
});
