import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_alunos():
    """Reseta a lista de alunos antes de cada teste."""
    client.delete("/api/v1/alunos/")
    yield


class TestCriarAlunos:
    """Testes de criação de alunos."""

    def test_criar_aluno_ges(self):
        """Cria um aluno do curso GES."""
        response = client.post("/api/v1/alunos/", json={
            "nome": "João Silva",
            "email": "joao@example.com",
            "curso": "GES"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "João Silva"
        assert data["email"] == "joao@example.com"
        assert data["curso"] == "GES"
        assert data["id"] == "GES1"
        assert data["matricula"] == 1

    def test_criar_aluno_gec(self):
        """Cria um aluno do curso GEC."""
        response = client.post("/api/v1/alunos/", json={
            "nome": "Maria Santos",
            "email": "maria@example.com",
            "curso": "GEC"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Maria Santos"
        assert data["email"] == "maria@example.com"
        assert data["curso"] == "GEC"
        assert data["id"] == "GEC1"
        assert data["matricula"] == 1

    def test_criar_tres_alunos_por_curso(self):
        """Cria 3 alunos por curso (GES e GEC)."""
        # Alunos GES
        alunos_ges = [
            {"nome": "Aluno GES 1", "email": "aluno1@example.com", "curso": "GES"},
            {"nome": "Aluno GES 2", "email": "aluno2@example.com", "curso": "GES"},
            {"nome": "Aluno GES 3", "email": "aluno3@example.com", "curso": "GES"}
        ]

        ids_ges = []
        for i, aluno in enumerate(alunos_ges):
            response = client.post("/api/v1/alunos/", json=aluno)
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == f"GES{i+1}"
            assert data["matricula"] == i+1
            ids_ges.append(data["id"])

        # Alunos GEC
        alunos_gec = [
            {"nome": "Aluno GEC 1", "email": "alunogec1@example.com", "curso": "GEC"},
            {"nome": "Aluno GEC 2", "email": "alunogec2@example.com", "curso": "GEC"},
            {"nome": "Aluno GEC 3", "email": "alunogec3@example.com", "curso": "GEC"}
        ]

        ids_gec = []
        for i, aluno in enumerate(alunos_gec):
            response = client.post("/api/v1/alunos/", json=aluno)
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == f"GEC{i+1}"
            assert data["matricula"] == i+1
            ids_gec.append(data["id"])

        # Total de 6 alunos criados
        response = client.get("/api/v1/alunos/")
        assert response.status_code == 200
        assert len(response.json()) == 6


class TestListarAlunos:
    """Testes de listagem de alunos."""

    def test_listar_alunos_vazio(self):
        """Lista alunos quando a lista está vazia."""
        response = client.get("/api/v1/alunos/")
        assert response.status_code == 200
        assert response.json() == []

    def test_listar_alunos_com_dados(self):
        """Lista alunos após criar alguns."""
        # Criar 2 alunos
        client.post("/api/v1/alunos/", json={
            "nome": "Aluno 1",
            "email": "aluno1@example.com",
            "curso": "GES"
        })
        client.post("/api/v1/alunos/", json={
            "nome": "Aluno 2",
            "email": "aluno2@example.com",
            "curso": "GEC"
        })

        response = client.get("/api/v1/alunos/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("id" in aluno for aluno in data)
        assert all("nome" in aluno for aluno in data)
        assert all("email" in aluno for aluno in data)


class TestBuscarAluno:
    """Testes de busca de aluno por ID."""

    def test_buscar_aluno_existente(self):
        """Busca um aluno que existe."""
        # Criar um aluno
        create_response = client.post("/api/v1/alunos/", json={
            "nome": "João Silva",
            "email": "joao@example.com",
            "curso": "GES"
        })
        aluno_id = create_response.json()["id"]

        # Buscar o aluno
        response = client.get(f"/api/v1/alunos/{aluno_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == aluno_id
        assert data["nome"] == "João Silva"

    def test_buscar_aluno_inexistente(self):
        """Tenta buscar um aluno que não existe."""
        response = client.get("/api/v1/alunos/GES999")
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]

    def test_buscar_diferentes_ids(self):
        """Busca diferentes alunos por seus IDs."""
        # Criar 3 alunos
        ids = []
        for i in range(3):
            response = client.post("/api/v1/alunos/", json={
                "nome": f"Aluno {i+1}",
                "email": f"aluno{i+1}@example.com",
                "curso": "GES"
            })
            ids.append(response.json()["id"])

        # Buscar cada aluno
        for aluno_id in ids:
            response = client.get(f"/api/v1/alunos/{aluno_id}")
            assert response.status_code == 200
            assert response.json()["id"] == aluno_id


class TestAtualizarAluno:
    """Testes de atualização de aluno."""

    def test_atualizar_aluno_nome(self):
        """Atualiza apenas o nome de um aluno."""
        # Criar aluno
        create_response = client.post("/api/v1/alunos/", json={
            "nome": "João Silva",
            "email": "joao@example.com",
            "curso": "GES"
        })
        aluno_id = create_response.json()["id"]

        # Atualizar nome
        response = client.patch(f"/api/v1/alunos/{aluno_id}", json={
            "nome": "João Santos"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "João Santos"
        assert data["email"] == "joao@example.com"

    def test_atualizar_aluno_email(self):
        """Atualiza apenas o email de um aluno."""
        # Criar aluno
        create_response = client.post("/api/v1/alunos/", json={
            "nome": "Maria Santos",
            "email": "maria@example.com",
            "curso": "GES"
        })
        aluno_id = create_response.json()["id"]

        # Atualizar email
        response = client.patch(f"/api/v1/alunos/{aluno_id}", json={
            "email": "maria.santos@example.com"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Maria Santos"
        assert data["email"] == "maria.santos@example.com"

    def test_atualizar_aluno_completo(self):
        """Atualiza nome e email de um aluno."""
        # Criar aluno
        create_response = client.post("/api/v1/alunos/", json={
            "nome": "Pedro Costa",
            "email": "pedro@example.com",
            "curso": "GEC"
        })
        aluno_id = create_response.json()["id"]

        # Atualizar dados
        response = client.patch(f"/api/v1/alunos/{aluno_id}", json={
            "nome": "Pedro Silva",
            "email": "pedro.silva@example.com"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Pedro Silva"
        assert data["email"] == "pedro.silva@example.com"

    def test_atualizar_aluno_inexistente(self):
        """Tenta atualizar um aluno que não existe."""
        response = client.patch("/api/v1/alunos/GES999", json={
            "nome": "Novo Nome"
        })
        assert response.status_code == 404


class TestDeletarAluno:
    """Testes de deleção de aluno."""

    def test_deletar_aluno_existente(self):
        """Deleta um aluno existente."""
        # Criar aluno
        create_response = client.post("/api/v1/alunos/", json={
            "nome": "Aluno para Deletar",
            "email": "deletar@example.com",
            "curso": "GES"
        })
        aluno_id = create_response.json()["id"]

        # Deletar aluno
        response = client.delete(f"/api/v1/alunos/{aluno_id}")
        assert response.status_code == 200
        assert "sucesso" in response.json()["mensagem"]

        # Verificar que foi deletado
        response = client.get(f"/api/v1/alunos/{aluno_id}")
        assert response.status_code == 404

    def test_deletar_aluno_inexistente(self):
        """Tenta deletar um aluno que não existe."""
        response = client.delete("/api/v1/alunos/GES999")
        assert response.status_code == 404

    def test_id_nao_reutilizado_apos_delecao(self):
        """Verifica que ID não é reutilizado após deleção de aluno."""
        # Criar dois alunos GES
        response1 = client.post("/api/v1/alunos/", json={
            "nome": "Primeiro",
            "email": "primeiro@example.com",
            "curso": "GES"
        })
        aluno1_id = response1.json()["id"]
        assert aluno1_id == "GES1"

        response2 = client.post("/api/v1/alunos/", json={
            "nome": "Segundo",
            "email": "segundo@example.com",
            "curso": "GES"
        })
        aluno2_id = response2.json()["id"]
        assert aluno2_id == "GES2"

        # Deletar primeiro aluno
        client.delete(f"/api/v1/alunos/{aluno1_id}")

        # Criar novo aluno GES
        response3 = client.post("/api/v1/alunos/", json={
            "nome": "Terceiro",
            "email": "terceiro@example.com",
            "curso": "GES"
        })
        aluno3_id = response3.json()["id"]
        # ID não deve ser GES1, deve ser GES3
        assert aluno3_id == "GES3"

    def test_deletar_alunos_com_listagem(self):
        """Deleta alunos e verifica a listagem."""
        # Criar 3 alunos
        ids = []
        for i in range(3):
            response = client.post("/api/v1/alunos/", json={
                "nome": f"Aluno {i+1}",
                "email": f"aluno{i+1}@example.com",
                "curso": "GES"
            })
            ids.append(response.json()["id"])

        # Verificar que há 3 alunos
        response = client.get("/api/v1/alunos/")
        assert len(response.json()) == 3

        # Deletar primeiro aluno
        client.delete(f"/api/v1/alunos/{ids[0]}")

        # Verificar que há 2 alunos
        response = client.get("/api/v1/alunos/")
        assert len(response.json()) == 2


class TestReset:
    """Testes de reset da lista de alunos."""

    def test_resetar_lista_alunos(self):
        """Reseta a lista de alunos."""
        # Criar alguns alunos
        for i in range(3):
            client.post("/api/v1/alunos/", json={
                "nome": f"Aluno {i+1}",
                "email": f"aluno{i+1}@example.com",
                "curso": "GES"
            })

        # Verificar que há alunos
        response = client.get("/api/v1/alunos/")
        assert len(response.json()) == 3

        # Resetar
        response = client.delete("/api/v1/alunos/")
        assert response.status_code == 200
        assert "sucesso" in response.json()["mensagem"]

        # Verificar que lista está vazia
        response = client.get("/api/v1/alunos/")
        assert response.json() == []
