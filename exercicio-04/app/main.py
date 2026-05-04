from fastapi import FastAPI

from app.routes.aluno_routes import router as aluno_router
from app.middlewares.request_logging import log_requests
from app.middlewares.custom_header import add_custom_header

app = FastAPI(
    title="Gerenciador de Alunos API",
    description="API para gerenciamento completo de alunos com operações CRUD",
    version="1.0.0"
)

app.middleware("http")(log_requests)
app.middleware("http")(add_custom_header)

app.include_router(aluno_router)

@app.get("/")
def root():
    return {"mensagem": "API de Gerenciamento de Alunos funcionando!"}