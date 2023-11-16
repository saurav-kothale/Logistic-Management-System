document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Make an API call to get the JWT token
    // Use fetch or any other method to send the credentials to your server

    fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Assuming the API returns a token in the "token" property
        const accessToken = data.access.access_token;

        // Store the token in localStorage
        localStorage.setItem("accessToken", accessToken);

        // Redirect to the dashboard page
        window.location.href = "http://127.0.0.1:5500/template/dashboard/index.html";
    })
    .catch(error => {
        console.error("Login failed:", error);
        // Handle login failure (show an error message, etc.)
    });
});