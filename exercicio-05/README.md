Gerenciador de Alunos - API com FastAPI + PostgreSQL
# Gerenciador de Alunos - API com FastAPI + PostgreSQL

API completa de gerenciamento de alunos desenvolvida com **FastAPI** e **PostgreSQL**, com geração automática de matrículas por curso e testes automatizados.

## Requisitos Atendidos

- Adaptado para PostgreSQL
- Sistema de matrícula sequencial por curso (GES e GEC) com controle de concorrência
- Testes automatizados completos e modulares
- Operações CRUD completas
- Persistência de dados validada

### Funcionalidades Principais

- Geração automática de ID e matrícula (`GES1`, `GES2`, `GEC1`, etc.)
- Controle transacional seguro de matrículas
- Validação de e-mail e cursos permitidos (GES/GEC)
- Atualização parcial via PATCH
- Reset completo da base via API

## Endpoints

| Método   | Endpoint                        | Descrição                        |
|----------|---------------------------------|----------------------------------|
| POST     | `/api/v1/alunos/`               | Criar novo aluno                 |
| GET      | `/api/v1/alunos/`               | Listar todos os alunos           |
| GET      | `/api/v1/alunos/{aluno_id}`     | Buscar aluno por ID              |
| PATCH    | `/api/v1/alunos/{aluno_id}`     | Atualizar dados do aluno         |
| DELETE   | `/api/v1/alunos/{aluno_id}`     | Deletar aluno                    |
| DELETE   | `/api/v1/alunos/`               | Resetar todos os alunos          |

Como Executar
-------------

1. Docker Compose (Recomendado):
   docker compose up --build

   API disponível em: http://localhost:8000
   Documentação: http://localhost:8000/docs

2. Executar apenas os testes:
   docker compose up --build tests

Testes Automatizados
--------------------
Comando para rodar:
   pytest tests/test_alunos.py -v

Testes disponíveis:
- test_criar_3_alunos_ges
- test_criar_3_alunos_gec
- test_listar_alunos
- test_buscar_aluno_por_id
- test_atualizar_aluno
- test_deletar_aluno
- test_reset_alunos

Estrutura do Projeto
--------------------
```
│   ├── schemas/ 
│   │   └── aluno.py 
│   ├── services/ 
│   │   └── aluno_service.py 
│   ├── routes/ 
│   │   └── aluno_routes.py 
│   └── middlewares/ 
├── tests/ 
│   └── test_alunos.py 
├── docker-compose.yml 
├── Dockerfile 
├── requirements.txt 
└── README.md 
```

Docker Compose Services
-----------------------
- api     → Aplicação FastAPI
- db      → PostgreSQL 15 (com volume persistente)
- tests   → Container dedicado para executar os testes

Exemplo de Uso - Criar Aluno
----------------------------
curl -X POST "http://localhost:8000/api/v1/alunos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Gabriel",
    "email": "joao@example.com",
    "curso": "GES"
  }'

Comportamento de Matrículas
---------------------------
- Matrículas são sequenciais por curso
- IDs seguem o padrão: GES1, GES2, GEC1, GEC2...
- A sequência NÃO reinicia após deleções (comportamento correto)