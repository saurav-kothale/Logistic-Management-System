document.getElementById("processButton").addEventListener("click", async function () {
    const formData = new FormData(document.getElementById("uploadForm"));

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            // Process successful response and provide download link
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "modified_data.xlsx";
            a.style.display = "none";
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            // Handle error response
            const errorMessage = await response.text();
            document.getElementById("message").textContent = "Error: " + errorMessage;
        }
    } catch (error) {
        console.error("Error:", error);
    }
});
