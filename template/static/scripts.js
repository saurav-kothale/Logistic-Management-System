document.getElementById("upload-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    
    const formData = new FormData(this);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            // Process successful response and provide download link
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.getElementById("download-link");
            a.href = url;
            a.style.display = "block";
        } else {
            // Handle error response
            console.error("Error:", response);
        }
    } catch (error) {
        console.error("Error:", error);
    }
});