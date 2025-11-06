import pytest
from app.app import app, reset_data

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        reset_data()  # Limpia y recarga los contactos precargados
        yield client

def test_listar_contactos(client):
    # Al iniciar, ya hay 3 contactos precargados
    res = client.get("/contacts")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 3
    nombres = [c["name"] for c in data]
    assert "Juan Pérez" in nombres
    assert "Ana López" in nombres
    assert "Carlos Díaz" in nombres

def test_crear_contacto(client):
    res = client.post("/contacts", json={"name": "Luis", "email": "luis@mail.com"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == "Luis"
    # Lista ahora tiene 4 contactos
    res2 = client.get("/contacts")
    assert len(res2.get_json()) == 4

def test_editar_contacto(client):
    # Editamos "Ana López" (id=2)
    res = client.put("/contacts/2", json={"phone": "111222333"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["phone"] == "111222333"

def test_eliminar_contacto(client):
    # Eliminamos "Carlos Díaz" (id=3)
    res = client.delete("/contacts/3")
    assert res.status_code == 200
    # Confirmamos eliminación
    res2 = client.get("/contacts/3")
    assert res2.status_code == 404

def test_obtener_contacto_inexistente(client):
    res = client.get("/contacts/999")
    assert res.status_code == 404

def test_crear_contacto_sin_campos(client):
    res = client.post("/contacts", json={"name": "SoloNombre"})
    assert res.status_code == 400
