// TODO: After deploying the CDK stack, replace the value below with the actual
// ApiURL output from the stack (e.g., "https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod").
// You can find this value by running: cdk deploy --outputs-file outputs.json
// Then copy the ApiURL value from that file into this variable.
const API_ENDPOINT = "API_ENDPOINT";

document.getElementById("nameForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const nameInput = document.getElementById("name");
    const resultDiv = document.getElementById("result");
    const submitButton = document.querySelector('button[type="submit"]');
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

    // Disable button during request to prevent duplicate submissions
    submitButton.disabled = true;

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
    } finally {
        submitButton.disabled = false;
    }
});
