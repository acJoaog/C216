from typing import List
from app.schemas.aluno import Aluno, AlunoCreate, AlunoUpdate

class AlunoService:
    def __init__(self):
        self._alunos: List[Aluno] = []
        self._matricula_counters = {"GES": 1, "GEC": 1}
        self._used_ids = set()

    def listar(self) -> List[Aluno]:
        """Lista todos os alunos."""
        return self._alunos

    def buscar_por_id(self, aluno_id: str) -> Aluno | None:
        """Busca um aluno pelo ID."""
        for aluno in self._alunos:
            if aluno.id == aluno_id:
                return aluno
        return None

    def criar(self, aluno_data: AlunoCreate) -> Aluno:
        """Cria um novo aluno com ID gerado automaticamente."""
        curso = aluno_data.curso
        matricula = self._matricula_counters[curso]
        aluno_id = f"{curso}{matricula}"
        
        novo_aluno = Aluno(
            id=aluno_id,
            nome=aluno_data.nome,
            email=aluno_data.email,
            curso=curso,
            matricula=matricula
        )
        
        self._alunos.append(novo_aluno)
        self._matricula_counters[curso] += 1
        self._used_ids.add(aluno_id)
        
        return novo_aluno

    def atualizar(self, aluno_id: str, aluno_data: AlunoUpdate) -> Aluno | None:
        """Atualiza dados de um aluno (PATCH)."""
        aluno = self.buscar_por_id(aluno_id)
        if not aluno:
            return None
        
        if aluno_data.nome is not None:
            aluno.nome = aluno_data.nome
        if aluno_data.email is not None:
            aluno.email = aluno_data.email
        # Nota: curso e matrícula não podem ser alterados
        
        return aluno

    def deletar(self, aluno_id: str) -> bool:
        """Remove um aluno do sistema."""
        aluno = self.buscar_por_id(aluno_id)
        if aluno:
            self._alunos.remove(aluno)
            # O ID não é reutilizado mesmo após deletar
            return True
        return False

    def reset(self) -> None:
        """Reseta a lista de alunos e contadores."""
        self._alunos = []
        self._matricula_counters = {"GES": 1, "GEC": 1}
        self._used_ids = set()
