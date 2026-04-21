import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}

def test_get_hello_query():
    response = client.get("/api/v1/hello?name=João")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello João"}

def test_get_hello_path():
    response = client.get("/api/v1/hello/João")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello João"}

def test_post_hello():
    response = client.post("/api/v1/hello", json={"name": "João"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello João"}

def test_put_update():
    response = client.put("/api/v1/update", json={"name": "João"})
    assert response.status_code == 200
    assert response.json() == {"message": "Recurso atualizado com o nome: João"}

def test_delete_user():
    response = client.delete("/api/v1/delete?name=João")
    assert response.status_code == 200
    assert response.json() == {"message": "Recurso deletado com o nome: João"}

def test_patch_user():
    response = client.patch("/api/v1/patch", json={"name": "João"})
    assert response.status_code == 200
    assert response.json() == {"message": "Modificação parcial aplicada ao recurso com o nome: João"}