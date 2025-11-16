# desafio-autou

Criar e ativar ambiente virtual

python -m venv .venv

Windows:

.venv\Scripts\activate

Linux / Mac:

source .venv/bin/activate

----
Instalar dependências

cd backend

pip install -r requirements.txt

----
Configurar variáveis de ambiente 

Edite o arquivo backend/.env e adicione sua chave da API:

GOOGLE_API_KEY=sua_chave_aqui

Obtenha sua chave em: https://aistudio.google.com/app/apikey

----
Executar o servidor backend:

uvicorn main:app --reload

O backend estará disponível em: http://localhost:8000

----
Configurar frontend

Em outro terminal:

cd frontend

python -m http.server 8080

O frontend estará disponível em:

http://localhost:8080
