from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_game():
    response = client.post(
        "/games/",
        json={
            "id": "game-test-1",
            "title": "The Legend of Zelda",
            "category": "Aventura",
            "price": 60.0,
            "release_date": "2023-05-12",
            "is_active": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "game-test-1"
    assert data["title"] == "The Legend of Zelda"

def test_get_games():
    response = client.get("/games/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_game_not_found():
    response = client.get("/games/id-falso-999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Videojuego no encontrado."

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "id": "user-test-1",
            "username": "gamer_pro",
            "email": "gamer@example.com",
            "is_active": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "gamer_pro"