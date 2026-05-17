import asyncpg
import os
from urllib.parse import urlparse

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/alunos_db"
)

async def get_connection():
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        # Fallback para desenvolvimento local
        database_url = "postgresql://postgres:password@localhost:5432/alunos_db"
    
    # Se estiver rodando dentro do Docker (detecta hostname 'db')
    if os.getenv("DOCKER_ENV") or "db" in database_url:
        # Já está configurado para Docker
        pass
    else:
        # Rodando localmente → força localhost
        if "host=db" in database_url or "db:" in database_url:
            database_url = database_url.replace("host=db", "host=localhost").replace("db:5432", "localhost:5432")
    
    try:
        return await asyncpg.connect(database_url)
    except Exception as e:
        print(f"Erro ao conectar no banco: {e}")
        print(f"URL utilizada: {database_url}")
        raise