from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_note():
    response = client.post("/notes", json={"title": "test", "body": "hello"})
    assert response.status_code == 200
    created = response.json()
    assert created["title"] == "test"

    response = client.get("/notes")
    assert response.status_code == 200
    assert any(n["id"] == created["id"] for n in response.json())
