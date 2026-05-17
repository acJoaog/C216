from fastapi import APIRouter, HTTPException
from app.schemas.aluno import Aluno, AlunoCreate, AlunoUpdate
from app.services.aluno_service import AlunoService

router = APIRouter(prefix="/api/v1/alunos", tags=["Alunos"])
service = AlunoService()

@router.post("/", response_model=Aluno)
async def criar_aluno(aluno: AlunoCreate):
    return await service.criar(aluno)

@router.get("/", response_model=list[Aluno])
async def listar_alunos():
    return await service.listar()

@router.get("/{aluno_id}", response_model=Aluno)
async def buscar_aluno(aluno_id: str):
    aluno = await service.buscar_por_id(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.patch("/{aluno_id}", response_model=Aluno)
async def atualizar_aluno(aluno_id: str, aluno: AlunoUpdate):
    atualizado = await service.atualizar(aluno_id, aluno)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return atualizado

@router.delete("/{aluno_id}")
async def deletar_aluno(aluno_id: str):
    sucesso = await service.deletar(aluno_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"mensagem": "Aluno deletado com sucesso"}

@router.delete("/")
async def resetar_alunos():
    await service.reset()
    return {"mensagem": "Lista de alunos resetada com sucesso"}