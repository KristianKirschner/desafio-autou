# Desafio AutoU

Este projeto foi desenvolvido como parte de um desafio técnico de um processo seletivo para estágio em Engenharia de Software na empresa Autou, com o objetivo de demonstrar habilidades em desenvolvimento full stack e integração com APIs de inteligência artificial.

As instruções exatas do desafio podem ser encontradas no seguinte link:  
https://autou-digital.notion.site/Contexto-do-Desafio-18836ce78e5580d0b59bcf9610b27769  

## Tecnologias Utilizadas

-   **Python**
-   **FastAPI**
-   **HTML, CSS e JavaScript**
-   **API Google AI (Gemini)**

------------------------------------------------------------------------

## Como Executar


## Configuração do Projeto

### Criar e ativar ambiente virtual

``` bash
python -m venv .venv
```

**Windows:**

``` bash
.venv\Scripts\activate
```

**Linux / Mac:**

``` bash
source .venv/bin/activate
```

------------------------------------------------------------------------

### Instalar dependências

``` bash
cd backend
pip install -r requirements.txt
```

------------------------------------------------------------------------

### Configurar variáveis de ambiente

Edite o arquivo `backend/.env` e adicione sua chave da API:

``` env
GOOGLE_API_KEY=sua_chave_aqui
```

Obtenha sua chave em:\
https://aistudio.google.com/app/apikey

------------------------------------------------------------------------

### Executar o servidor backend

``` bash
uvicorn main:app --reload
```

O backend estará disponível em:\
http://localhost:8000

------------------------------------------------------------------------

### Configurar frontend

Em outro terminal:

``` bash
cd frontend
python -m http.server 8080
```

O frontend estará disponível em:\
http://localhost:8080

------------------------------------------------------------------------

## Funcionalidades

-   Integração com API de inteligência artificial
-   Comunicação entre frontend e backend
-   Interface web simples para interação
-   Uso de variáveis de ambiente para segurança

