const form = document.getElementById("emailForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const textInput = document.getElementById("textInput");

    const formData = new FormData();
    if (fileInput.files.length > 0) {
        formData.append("file", fileInput.files[0]);
    }
    if (textInput.value.trim() !== "") {
        formData.append("text", textInput.value.trim());
    }


    const API_URL = "https://refactored-garbanzo-5p9jjppxg6gh76j6-8000.app.github.dev/classify/"
    const response = await fetch(API_URL, { 
        method: "POST",
        body: formData
    });

    const data = await response.json();
    document.getElementById("categoria").innerText = data.categoria || "Erro";
    document.getElementById("resposta").innerText = data.resposta_sugerida || "Erro";
});