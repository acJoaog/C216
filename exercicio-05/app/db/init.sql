DROP TABLE IF EXISTS alunos;
DROP TABLE IF EXISTS contadores;

CREATE TABLE IF NOT EXISTS alunos (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    curso TEXT NOT NULL,
    matricula INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS contadores (
    curso TEXT PRIMARY KEY,
    proximo_matricula INTEGER NOT NULL
);