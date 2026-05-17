from pydantic import BaseModel, EmailStr
from typing import Literal

class AlunoCreate(BaseModel):
    nome: str
    email: EmailStr
    curso: Literal["GES", "GEC"]

class Aluno(BaseModel):
    id: str
    nome: str
    email: str
    curso: Literal["GES", "GEC"]
    matricula: int

class AlunoUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    curso: Literal["GES", "GEC"] | None = None
