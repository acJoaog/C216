# Exercício 06 - Integração Frontend e Backend de Alunos

Projeto com frontend Flask e backend FastAPI para gerenciamento de alunos.

## Descrição

- `backend/`: API FastAPI para CRUD de alunos com PostgreSQL.
- `frontend/`: interface Flask simples que consome a API de alunos.
- `docker-compose.yml`: orquestra backend, banco e frontend.

## Como executar

### Usando Docker Compose

```bash
docker compose up --build
```

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

### Executar apenas o backend localmente

```bash
cd exercicio-06/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Executar apenas o frontend localmente

```bash
cd exercicio-06/frontend
pip install flask
python app.py
```

## Endpoints do Backend

| Método | Endpoint                        | Descrição                         |
|--------|---------------------------------|-----------------------------------|
| POST   | `/api/v1/alunos/`               | Criar novo aluno                  |
| GET    | `/api/v1/alunos/`               | Listar todos os alunos            |
| GET    | `/api/v1/alunos/{aluno_id}`     | Buscar aluno por ID               |
| PATCH  | `/api/v1/alunos/{aluno_id}`     | Atualizar dados do aluno          |
| DELETE | `/api/v1/alunos/{aluno_id}`     | Deletar aluno                     |
| DELETE | `/api/v1/alunos/`               | Resetar todos os alunos           |

## Rotas do Frontend

- `/` - página inicial
- `/about` - sobre o projeto
- `/contact` - contato
- `/alunos` - lista de alunos e formulário de cadastro/edição

## Testes

No backend, os testes estão em `backend/tests/test_alunos.py`.

```bash
cd exercicio-06/backend
python -m pytest -q backend/tests
```

## Observações

- O frontend consome a API do backend.
- A biblioteca `pytest_asyncio` está configurada no backend para testes assíncronos.
- Use `BACKEND_URL` no frontend se precisar apontar para outro host do backend.
