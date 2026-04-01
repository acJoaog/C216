# Exercicio 02 - Gerenciamento de Alunos

Este projeto implementa um CRUD (Criar, Ler, Atualizar, Excluir) de alunos via linha de comando em Python.

## Estrutura do repositório

- `app.py` - lógica do sistema de cadastro de alunos.
- `Dockerfile` - imagem Docker para rodar a aplicação.
- `requirements.txt` - dependências (atualmente vazio).

## Requisitos

- Python 3.10+
- Docker (opcional)

## Como usar localmente

1. Navegue até a pasta:

   ```bash
   cd exercicio-02
   ```

2. Execute o app:

   ```bash
   python app.py
   ```

3. No menu, escolha a opção desejada:

   1. Criar aluno
   2. Listar alunos
   3. Atualizar aluno
   4. Excluir aluno
   5. Sair

### Regras de matrícula

- Curso deve ser um dos seguintes: `GES`, `GEC`, `GET`, `GEP`.
- Matrícula gerada como `<CURSO><N>`, onde `N` é sequencial por curso.

## Como usar com Docker

1. Build da imagem:

   ```bash
   docker build -t professores-app .
   ```

2. Rodar container:

   ```bash
   docker run -it --rm professores-app
   ```

3. Use o menu interativo no terminal.

## Teste rápido

- Adicione um aluno no curso `GES`. Se for o primeiro, matrícula deve ser `GES1`.
- Adicione outro no mesmo curso, matrícula deve ser `GES2`.
- Tente curso inválido para ver mensagem de erro.

