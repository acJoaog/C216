from fastapi import APIRouter, HTTPException
from app.schemas.aluno import Aluno, AlunoCreate, AlunoUpdate
from app.services.aluno_service import AlunoService

router = APIRouter(prefix="/api/v1/alunos", tags=["Alunos"])
service = AlunoService()

@router.post("/", response_model=Aluno)
def criar_aluno(aluno: AlunoCreate):
    """Cadastra um novo aluno."""
    return service.criar(aluno)

@router.get("/", response_model=list[Aluno])
def listar_alunos():
    """Lista todos os alunos."""
    return service.listar()

@router.get("/{aluno_id}", response_model=Aluno)
def buscar_aluno(aluno_id: str):
    """Busca um aluno pelo ID."""
    aluno = service.buscar_por_id(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.patch("/{aluno_id}", response_model=Aluno)
def atualizar_aluno(aluno_id: str, aluno: AlunoUpdate):
    """Atualiza dados de um aluno."""
    atualizado = service.atualizar(aluno_id, aluno)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return atualizado

@router.delete("/{aluno_id}")
def deletar_aluno(aluno_id: str):
    """Remove um aluno do sistema."""
    sucesso = service.deletar(aluno_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"mensagem": "Aluno deletado com sucesso"}

@router.delete("/")
def resetar_alunos():
    """Reseta a lista de alunos."""
    service.reset()
    return {"mensagem": "Lista de alunos resetada com sucesso"}
