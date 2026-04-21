# Exercicio 03 - API FastAPI com Testes

Este projeto implementa uma API REST usando FastAPI com endpoints que demonstram os principais métodos HTTP (GET, POST, PUT, DELETE, PATCH).

## Estrutura do repositório

- `app/main.py` - implementação da API FastAPI
- `tests/main-test.py` - testes automatizados com pytest
- `Dockerfile` - imagem Docker para rodar a aplicação
- `docker-compose.yml` - orquestração de containers
- `requirements.txt` - dependências do projeto

## Requisitos

- Python 3.10+
- FastAPI
- Uvicorn
- Pytest
- Docker (opcional)

## Como usar localmente

1. Navegue até a pasta:

   ```bash
   cd exercicio-03
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute a API:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Acesse a documentação interativa em `http://localhost:8000/docs`

## Endpoints disponíveis

- `GET /` - Retorna mensagem de boas-vindas
- `GET /api/v1/hello?name=<name>` - Saudação via query parameter
- `GET /api/v1/hello/<name>` - Saudação via path parameter
- `POST /api/v1/hello` - Saudação com dados no corpo da requisição
- `PUT /api/v1/update` - Atualiza um recurso
- `DELETE /api/v1/delete?name=<name>` - Deleta um recurso
- `PATCH /api/v1/patch` - Modifica parcialmente um recurso

## Como executar os testes

```bash
pytest tests/main-test.py -v
```

## Como usar com Docker

1. Build da imagem:

   ```bash
   docker build -t fastapi-app .
   ```

2. Rodar container:

   ```bash
   docker run -p 8000:8000 fastapi-app
   ```

## Docker Compose

1. Inicie os containers:

   ```bash
   docker-compose up
   ```

2. A API estará disponível em `http://localhost:8000`

