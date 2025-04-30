from app.core.security import get_current_user
from sqlmodel import Session
from tests.conftest import engine
from app.models.models import URL

def test_create_short_link(client, user):
    """Проверка, что короткая ссылка создаётся и сохраняется в БД."""
    def override_user():
        return user
    client.app.dependency_overrides[get_current_user] = override_user

    payload = {"user_url": "https://example.com"}
    response = client.post("/short_link", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data

    # Извлекаем ID из URL
    short_id = data["short_url"].rstrip("/").split("/")[-1]

    # Проверка содержимого базы
    with Session(engine) as session:
        url = session.get(URL, short_id)
        assert url is not None
        assert url.original_url == "https://example.com"
        assert url.owner == user.username
        assert url.clicks == 0