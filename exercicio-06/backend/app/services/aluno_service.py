from typing import List
from app.db.connection import get_connection
from app.schemas.aluno import Aluno, AlunoCreate, AlunoUpdate


class AlunoService:

    async def listar(self) -> List[Aluno]:
        """Lista todos os alunos do banco."""
        conn = await get_connection()
        try:
            rows = await conn.fetch("SELECT * FROM alunos ORDER BY id")
            return [Aluno(**dict(row)) for row in rows]
        finally:
            await conn.close()

    async def buscar_por_id(self, aluno_id: str) -> Aluno | None:
        """Busca um aluno pelo ID."""
        conn = await get_connection()
        try:
            row = await conn.fetchrow(
                "SELECT * FROM alunos WHERE id = $1", aluno_id
            )
            return Aluno(**dict(row)) if row else None
        finally:
            await conn.close()

    async def criar(self, aluno_data: AlunoCreate) -> Aluno:
        """Cria um novo aluno com ID gerado automaticamente."""
        conn = await get_connection()
        try:
            async with conn.transaction():
                # Garante que existe um contador para o curso
                await conn.execute(
                    """
                    INSERT INTO contadores (curso, proximo_matricula)
                    VALUES ($1, 1)
                    ON CONFLICT (curso) DO NOTHING
                    """,
                    aluno_data.curso
                )

                # Obtém e bloqueia a linha do contador para o curso
                row = await conn.fetchrow(
                    """
                    SELECT proximo_matricula
                    FROM contadores
                    WHERE curso = $1
                    FOR UPDATE
                    """,
                    aluno_data.curso
                )
                matricula = row["proximo_matricula"]
                aluno_id = f"{aluno_data.curso}{matricula}"

                # Insere o aluno
                await conn.execute(
                    """
                    INSERT INTO alunos (id, nome, email, curso, matricula)
                    VALUES ($1, $2, $3, $4, $5)
                    """,
                    aluno_id, aluno_data.nome, aluno_data.email,
                    aluno_data.curso, matricula
                )

                # Incrementa o contador
                await conn.execute(
                    """
                    UPDATE contadores
                    SET proximo_matricula = proximo_matricula + 1
                    WHERE curso = $1
                    """,
                    aluno_data.curso
                )

            # Retorna o aluno recém-criado
            return Aluno(
                id=aluno_id,
                nome=aluno_data.nome,
                email=aluno_data.email,
                curso=aluno_data.curso,
                matricula=matricula
            )
        finally:
            await conn.close()

    async def atualizar(self, aluno_id: str, aluno_data: AlunoUpdate) -> Aluno | None:
        """Atualiza dados de um aluno (PATCH)."""
        conn = await get_connection()
        try:
            # Monta a query dinamicamente apenas com os campos fornecidos
            updates = []
            params = []
            if aluno_data.nome is not None:
                updates.append("nome = $1")
                params.append(aluno_data.nome)
            if aluno_data.email is not None:
                updates.append("email = $2")
                params.append(aluno_data.email)

            if not updates:
                # Nada para atualizar -> apenas busca o aluno
                row = await conn.fetchrow(
                    "SELECT * FROM alunos WHERE id = $1", aluno_id
                )
                return Aluno(**dict(row)) if row else None

            # Adiciona o id como último parâmetro
            params.append(aluno_id)
            query = f"""
                UPDATE alunos
                SET {', '.join(updates)}
                WHERE id = ${len(params)}
                RETURNING *
            """
            row = await conn.fetchrow(query, *params)
            return Aluno(**dict(row)) if row else None
        finally:
            await conn.close()

    async def deletar(self, aluno_id: str) -> bool:
        """Remove um aluno do sistema."""
        conn = await get_connection()
        try:
            result = await conn.execute(
                "DELETE FROM alunos WHERE id = $1", aluno_id
            )
            return result == "DELETE 1"
        finally:
            await conn.close()

    async def reset(self) -> None:
        """Reseta a lista de alunos e os contadores."""
        conn = await get_connection()
        try:
            async with conn.transaction():
                await conn.execute("DELETE FROM alunos")
                await conn.execute(
                    "UPDATE contadores SET proximo_matricula = 1"
                )
        finally:
            await conn.close()