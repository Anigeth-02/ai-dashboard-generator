async function generateDashboard() {
    alert("Button clicked!");
    const jsonInput = document.getElementById("jsonInput").value;
    const promptInput = document.getElementById("promptInput").value;
    const preview = document.getElementById("preview");

    const response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            json: jsonInput,
            prompt: promptInput
        })
    });

    const result = await response.json();

    if (result.error) {
        alert(result.error);
        return;
    }

    preview.srcdoc = result.html;
}
