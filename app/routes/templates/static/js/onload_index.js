window.addEventListener("load", async function() {
    const csrf_resp = await fetch("/application/directory/v1/controller/security/csrf-token", {
        method: "POST",
        credentials: "same-origin",
    });
    if (csrf_resp.ok) {
        // if the request is successful, parse the json response
        // const data = await csrf_resp.json();
        x_csrf_token = csrf_resp.headers.get("X-CSRF-Token");
        document.headers = `X-CSRF-Token=${x_csrf_token}; path=/; SameSite=strict`;
    } else {
        console.error(csrf_resp.statusText);
    }
})