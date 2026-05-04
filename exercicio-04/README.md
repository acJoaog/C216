# Gerenciador de Alunos - API com FastAPI

API completa de CRUD para gerenciamento de alunos usando FastAPI, com suporte a múltiplos cursos (GES e GEC).

## Requisitos Atendidos

**Endpoints CRUD Completos:**
- `POST /api/v1/alunos/` - Cadastra um novo aluno
- `GET /api/v1/alunos/` - Lista todos os alunos
- `GET /api/v1/alunos/{aluno_id}` - Busca um aluno pelo ID
- `PATCH /api/v1/alunos/{aluno_id}` - Atualiza dados de um aluno
- `DELETE /api/v1/alunos/{aluno_id}` - Remove um aluno do sistema
- `DELETE /api/v1/alunos/` - Reseta a lista de alunos

**Atributos de Aluno:**
- Nome
- E-mail (validado)
- Curso (GES ou GEC)
- Matrícula (gerada automaticamente por curso: 1, 2, 3, etc.)
- ID (curso + matrícula sequencial, ex: GES1, GES2, GEC1, GEC2)
- **IDs não são reutilizados após deleção**

**Testes Automatizados:**
- 3 alunos por curso (GES e GEC)
- Listagem de alunos
- Busca por ID
- Atualização de dados
- Remoção de alunos
- Teste de IDs não reutilizados

**Docker Compose:**
- API containerizada e pronta para produção

## Como Executar

### Com Docker Compose (Recomendado)

```bash
docker-compose up
```

A API estará disponível em: `http://localhost:8000`
Documentação interativa: `http://localhost:8000/docs`

### Localmente (Sem Docker)

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
uvicorn app.main:app --reload

# Em outro terminal, executar testes
pytest tests/test_alunos.py -v
```

## Exemplos de Uso

### Criar um aluno

```bash
curl -X POST "http://localhost:8000/api/v1/alunos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Gabriel",
    "email": "joao@example.com",
    "curso": "GES"
  }'
```

**Resposta:**
```json
{
  "id": "GES1",
  "nome": "João Gabriel",
  "email": "joao@example.com",
  "curso": "GES",
  "matricula": 1
}
```

### Listar todos os alunos

```bash
curl "http://localhost:8000/api/v1/alunos/"
```

### Buscar aluno por ID

```bash
curl "http://localhost:8000/api/v1/alunos/GES1"
```

### Atualizar um aluno

```bash
curl -X PATCH "http://localhost:8000/api/v1/alunos/GES1" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Santos",
    "email": "joao.santos@example.com"
  }'
```

### Deletar um aluno

```bash
curl -X DELETE "http://localhost:8000/api/v1/alunos/GES1"
```

### Resetar lista de alunos

```bash
curl -X DELETE "http://localhost:8000/api/v1/alunos/"
```

## Testes

```bash
# Executar todos os testes
pytest tests/test_alunos.py -v

# Executar teste específico
pytest tests/test_alunos.py::TestCriarAlunos -v

# Com cobertura
pytest tests/test_alunos.py -v --cov=app
```

## Estrutura do Projeto

```
exercicio-04/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação FastAPI
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── aluno.py           # Modelos Pydantic
│   ├── services/
│   │   ├── __init__.py
│   │   └── aluno_service.py   # Lógica de negócio
│   ├── routes/
│   │   ├── __init__.py
│   │   └── aluno_routes.py    # Endpoints
│   └── middlewares/
│       ├── __init__.py
│       ├── logging.py
│       └── custom_header.py
├── tests/
│   ├── __init__.py
│   └── test_alunos.py         # Testes automatizados
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Comportamento de IDs

Os IDs são gerados automaticamente no formato: `{CURSO}{NÚMERO_SEQUENCIAL}`

Exemplos:
- Primeiro aluno GES: `GES1`
- Segundo aluno GES: `GES2`
- Primeiro aluno GEC: `GEC1`
- Segundo aluno GEC: `GEC2`

**Importante:** Mesmo que um aluno seja deletado, seu ID não é reutilizado. Se `GES1` for deletado, o próximo aluno GES terá o ID `GES3` (ou superior, dependendo da sequência).

## Middlewares

A aplicação inclui middlewares para:
- Logging de requisições
- Adição de headers customizados

Veja os arquivos em `app/middlewares/` para mais detalhes.

## Documentação Interativa

Com a aplicação rodando, acesse:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
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
   docker-compose up -d --build
   ```

2. A API estará disponível em `http://localhost:8000`

