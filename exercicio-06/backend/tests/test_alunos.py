import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture(scope="function")
async def client():
    """Cliente de testes ASGI"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function", autouse=True)
async def reset_database(client):
    """Reseta o banco antes de cada teste"""
    try:
        resp = await client.delete("/api/v1/alunos/")
        if resp.status_code != 200:
            print(f"Reset falhou com status {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"Erro no reset: {e}")
        # Fallback: tentar reset direto no banco se a API falhar
        await reset_database_directly()


# ====================== TESTES DE CRIAÇÃO ======================

async def test_criar_3_alunos_ges(client):
    """Cria 3 alunos do curso GES"""
    alunos = [
        {"nome": "João Silva", "email": "joao@exemplo.com", "curso": "GES"},
        {"nome": "Maria Oliveira", "email": "maria@exemplo.com", "curso": "GES"},
        {"nome": "Pedro Santos", "email": "pedro@exemplo.com", "curso": "GES"},
    ]

    for aluno in alunos:
        resp = await client.post("/api/v1/alunos/", json=aluno)
        assert resp.status_code == 200
        data = resp.json()
        assert data["curso"] == "GES"
        assert data["id"].startswith("GES")
        assert data["matricula"] is not None


async def test_criar_3_alunos_gec(client):
    """Cria 3 alunos do curso GEC"""
    alunos = [
        {"nome": "Ana Costa", "email": "ana@exemplo.com", "curso": "GEC"},
        {"nome": "Lucas Mendes", "email": "lucas@exemplo.com", "curso": "GEC"},
        {"nome": "Julia Ferreira", "email": "julia@exemplo.com", "curso": "GEC"},
    ]

    for aluno in alunos:
        resp = await client.post("/api/v1/alunos/", json=aluno)
        assert resp.status_code == 200
        data = resp.json()
        assert data["curso"] == "GEC"
        assert data["id"].startswith("GEC")


# ====================== TESTES DE CONSULTA ======================

async def test_listar_alunos(client):
    """Testa listagem de alunos"""
    # Prepara dados
    await client.post("/api/v1/alunos/", json={"nome": "Teste Lista", "email": "lista@test.com", "curso": "GES"})
    
    resp = await client.get("/api/v1/alunos/")
    assert resp.status_code == 200
    alunos = resp.json()
    assert len(alunos) >= 1
    assert isinstance(alunos, list)


async def test_buscar_aluno_por_id(client):
    """Testa busca por ID"""
    # Cria um aluno
    resp = await client.post("/api/v1/alunos/", json={
        "nome": "Aluno Busca", 
        "email": "busca@test.com", 
        "curso": "GES"
    })
    aluno_id = resp.json()["id"]

    # Busca
    resp = await client.get(f"/api/v1/alunos/{aluno_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == aluno_id
    assert data["nome"] == "Aluno Busca"


# ====================== TESTES DE ALTERAÇÃO ======================

async def test_atualizar_aluno(client):
    """Testa atualização de dados (PATCH)"""
    # Cria aluno
    resp = await client.post("/api/v1/alunos/", json={
        "nome": "Aluno Antigo", 
        "email": "antigo@test.com", 
        "curso": "GES"
    })
    aluno_id = resp.json()["id"]

    # Atualiza
    update_data = {"nome": "Aluno Atualizado", "email": "novo@email.com"}
    resp = await client.patch(f"/api/v1/alunos/{aluno_id}", json=update_data)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["nome"] == "Aluno Atualizado"
    assert updated["email"] == "novo@email.com"


# ====================== TESTES DE REMOÇÃO ======================

async def test_deletar_aluno(client):
    """Testa remoção de aluno"""
    # Cria aluno
    resp = await client.post("/api/v1/alunos/", json={
        "nome": "Aluno Para Deletar", 
        "email": "deletar@test.com", 
        "curso": "GES"
    })
    aluno_id = resp.json()["id"]

    # Deleta
    resp = await client.delete(f"/api/v1/alunos/{aluno_id}")
    assert resp.status_code == 200

    # Verifica se foi deletado
    resp = await client.get(f"/api/v1/alunos/{aluno_id}")
    assert resp.status_code == 404


async def test_reset_alunos(client):
    """Testa reset completo da lista"""
    # Cria alguns alunos
    await client.post("/api/v1/alunos/", json={"nome": "Teste 1", "email": "t1@test.com", "curso": "GES"})
    await client.post("/api/v1/alunos/", json={"nome": "Teste 2", "email": "t2@test.com", "curso": "GEC"})

    # Reset
    resp = await client.delete("/api/v1/alunos/")
    assert resp.status_code == 200
    assert resp.json()["mensagem"] == "Lista de alunos resetada com sucesso"

    # Verifica se realmente resetou
    resp = await client.get("/api/v1/alunos/")
    assert len(resp.json()) == 0


# ====================== AUX ======================

async def reset_database_directly():
    """Fallback direto no banco (útil para testes locais)"""
    from app.db.connection import get_connection
    conn = await get_connection()
    try:
        await conn.execute("DELETE FROM alunos")
        await conn.execute("UPDATE contadores SET proximo_matricula = 1")
        print("Reset direto no banco realizado")
    finally:
        await conn.close()