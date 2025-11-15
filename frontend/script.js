const form = document.getElementById("emailForm");
const categoriaEl = document.getElementById("categoria");
const respostaEl = document.getElementById("resposta");

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

    const API_URL = "http://localhost:8000/classify/"
    
    try {
        const response = await fetch(API_URL, { 
            method: "POST",
            body: formData
        });

        const data = await response.json();
        categoriaEl.innerText = data.categoria || "Erro";
        respostaEl.innerText = data.resposta_sugerida || "Erro";

        // Salvar no histórico local
        saveToHistory({
            texto: textInput.value || (fileInput.files[0]?.name || ""),
            categoria: data.categoria || "Erro",
            resposta: data.resposta_sugerida || "Erro",
            timestamp: new Date().toLocaleString()
        });

        renderHistory();

    } catch (err) {
        console.error("Erro ao classificar email:", err);
    }
});

// Função do localStorage
function saveToHistory(entry) {
    let history = JSON.parse(localStorage.getItem("emailHistory")) || [];
    history.unshift(entry); 
    localStorage.setItem("emailHistory", JSON.stringify(history));
}

// Função para renderizar histórico
function renderHistory() {
    let history = JSON.parse(localStorage.getItem("emailHistory")) || [];
    let historyContainer = document.getElementById("history");

    if (!historyContainer) {
        historyContainer = document.createElement("div");
        historyContainer.id = "history";
        historyContainer.style.marginTop = "30px";
        historyContainer.innerHTML = "<h2>Histórico de Classificações:</h2>";
        document.querySelector(".container").appendChild(historyContainer);
    }

    historyContainer.innerHTML = "<h2>Histórico de Classificações:</h2>";

    history.forEach(item => {
        const div = document.createElement("div");
        div.style.border = "1px solid #ddd";
        div.style.borderRadius = "8px";
        div.style.padding = "10px";
        div.style.marginBottom = "10px";
        div.style.background = "#f9f9f9";

        div.innerHTML = `
            <p><strong>Data:</strong> ${item.timestamp}</p>
            <p><strong>Texto/Arquivo:</strong> ${item.texto}</p>
            <p><strong>Categoria:</strong> ${item.categoria}</p>
            <p><strong>Resposta:</strong> ${item.resposta}</p>
        `;
        historyContainer.appendChild(div);
    });
}

// Renderiza histórico ao carregar a página
renderHistory();
