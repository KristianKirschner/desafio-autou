from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json
import PyPDF2
from io import BytesIO

# Importações do gemini
from google import genai
from google.genai import types 

# --- Configuração Global ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não foi encontrada.")
    
client = genai.Client(api_key=GOOGLE_API_KEY)


app = FastAPI(
    title="Classificador de Email Gemini",
    description="API que classifica emails em Produtivo/Improdutivo usando a API Gemini."
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- Funções Auxiliares ---

def read_file(file_content: bytes, filename: str) -> str | None:
    """Lê o conteúdo de um arquivo .txt ou .pdf."""
    
    if filename.endswith(".txt"):
        try:
            # Tenta decodificar como UTF-8, o padrão mais comum
            return file_content.decode("utf-8")
        except UnicodeDecodeError:
            # Em caso de erro, tenta decodificar como Latin-1
            return file_content.decode("latin-1")
            
    elif filename.endswith(".pdf"):
        # Usa BytesIO para tratar o conteúdo em bytes como um arquivo
        pdf_file = BytesIO(file_content)
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # Extrai o texto de todas as páginas
            return "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
        except Exception as e:
            # Log ou tratamento de erro na leitura do PDF
            print(f"Erro ao ler PDF: {e}")
            return None
    
    return None

# --- Endpoint ---

@app.post("/classify/")
async def classify_email(
    file: UploadFile = File(None), 
    text: str = Form(None)
):
    """
    Classifica um email (enviado via arquivo ou texto direto) usando o modelo Gemini.
    Retorna uma categoria (Produtivo/Improdutivo) e uma sugestão de resposta.
    """
    email_text = ""
    
    # 1. Obter o texto do email
    if file:
        file_content = await file.read() # O método 'read' em UploadFile deve ser chamado com 'await'
        email_text = read_file(file_content, file.filename)
        
        if email_text is None or not email_text.strip():
            # Erro de formato ou arquivo vazio
            raise HTTPException(
                status_code=400, 
                detail="Formato de arquivo não suportado (.txt ou .pdf) ou arquivo vazio/ilegível."
            )
            
    elif text:
        email_text = text
    else:
        raise HTTPException(
            status_code=400, 
            detail="Nenhum texto ou arquivo enviado. Por favor, forneça o parâmetro 'text' ou 'file'."
        )

    # 2. Definir o prompt para o modelo
    prompt = f"""
Você é um assistente que classifica emails em 'Produtivo' ou 'Improdutivo' e sugere uma resposta adequada.
O formato de saída DEVE ser **JSON válido**. Não inclua nenhum texto de introdução ou explicação, apenas o objeto JSON.

Email: \"\"\"{email_text}\"\"\"

JSON esperado:
{{
  "categoria": "<Produtivo ou Improdutivo>",
  "resposta_sugerida": "<Sugestão de resposta apropriada>"
}}
"""

    # 3. Chamar a API Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Usando um modelo atual e rápido
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                max_output_tokens=500,
                response_mime_type="application/json" # Força a saída JSON se o modelo suportar
            )
        )
        
        # Tenta carregar o texto de resposta como JSON
        text_response = response.text.strip()
        data = json.loads(text_response)

    except Exception as e:
        # Erro na chamada da API ou no parse do JSON
        print(f"Erro na chamada da API/JSON: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro de processamento da API Gemini: {str(e)}"
        )
        
    # 4. Retornar a classificação
    return data