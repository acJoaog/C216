# Exercício 01 - Sistema de Gerenciamento de Alunos

Este é um programa simples em Python para gerenciar alunos de diferentes cursos.

## Funcionalidades

- **Criar Aluno**: Permite adicionar um novo aluno com nome, email e curso. Gera automaticamente uma matrícula única baseada no curso.
- **Listar Alunos**: Exibe todos os alunos cadastrados com suas informações.
- **Buscar por Matrícula**: Permite buscar um aluno específico pela matrícula.

## Cursos Suportados

- GES
- GEC
- GET
- GEP

## Como Executar

1. Certifique-se de ter Python instalado.
2. Execute o arquivo `main.py` no terminal:

   ```
   python main.py
   ```

3. Siga as instruções no console para interagir com o programa.

## Estrutura do Código

- `get_next_matricula_num(alunos, curso)`: Calcula o próximo número de matrícula para um curso.
- `criar_aluno(alunos)`: Cria um novo aluno com entrada do usuário.
- `listar_alunos(alunos)`: Lista todos os alunos.
- `buscar_matricula(alunos, matricula)`: Busca um aluno por matrícula.