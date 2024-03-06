document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("LoginFormUser");
    
    loginForm.addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        
        try {
            const response = await fetch("/application/api/v1/directory/authentication/tokenizer", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({
                    username: username,
                    password: password
                })
            });
            
            if (response.ok) {
                // Authentication successful
                // const tokenData = await response.json();
                window.location.reload();
            } else {
                // Authentication failed
                const errorData = await response.json();
                console.error("Authentication failed:", errorData.detail);
                // Display error message to the user
                document.getElementById("loginResult").textContent = "Authentication failed: " + errorData.detail;
            }
        } catch (error) {
            console.error("Error:", error);
            // Display error message to the user
            document.getElementById("loginResult").textContent = "Error: " + error.message;
        }
    });
});