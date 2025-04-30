import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.models.models import User
from app.db.session import get_session
from app.core.security import verify_password

from tests.conftest import engine

def test_register_user(client):
    """Проверка регистрации нового пользователя и записи в БД."""
    response = client.post("/register", params={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json() == {"message": "Пользователь зарегистрирован"}

    # Проверяем в БД
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == "testuser")).first()
        assert user is not None
        assert user.username == "testuser"
        assert verify_password("testpass", user.hashed_password)


def test_register_existing_user(client):
    """Попытка регистрации уже существующего пользователя."""
    response = client.post("/register", params={"username": "testuser", "password": "newpass"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Пользователь уже существует"


def test_login_success(client):
    """Проверка успешной авторизации и получения токена."""
    data = {"username": "testuser", "password": "testpass"}
    response = client.post("/token", data=data)
    assert response.status_code == 200
    json = response.json()
    assert "access_token" in json
    assert json["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Ошибка входа при неверном пароле."""
    data = {"username": "testuser", "password": "wrongpass"}
    response = client.post("/token", data=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Неверный логин или пароль"


def test_login_nonexistent_user(client):
    """Ошибка входа при несуществующем пользователе."""
    data = {"username": "ghostuser", "password": "ghostpass"}
    response = client.post("/token", data=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Неверный логин или пароль"