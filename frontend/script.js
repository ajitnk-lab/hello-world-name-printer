const API_ENDPOINT = "API_ENDPOINT";

document.getElementById("nameForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const nameInput = document.getElementById("name");
    const resultDiv = document.getElementById("result");
    const name = nameInput.value.trim();

    // Clear previous result
    resultDiv.textContent = "";
    resultDiv.className = "";

    // Validate input
    if (!name) {
        resultDiv.textContent = "Please enter a valid name.";
        resultDiv.className = "error";
        return;
    }

    try {
        const response = await fetch(`${API_ENDPOINT}/submit`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name: name })
        });

        if (!response.ok) {
            const errorData = await response.json();
            resultDiv.textContent = errorData.message || "Something went wrong. Please try again.";
            resultDiv.className = "error";
            return;
        }

        const data = await response.json();
        resultDiv.textContent = data.greeting;
        resultDiv.className = "success";
    } catch (error) {
        resultDiv.textContent = "Unable to connect to the server. Please try again later.";
        resultDiv.className = "error";
    }
});
