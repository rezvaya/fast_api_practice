import pytest
from sqlmodel import create_engine, SQLModel
from sqlmodel import Session
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import get_session

DB_URL = 'sqlite:///./test.db'
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope="module", autouse=True)
def prepare_database():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def user():
    class FakeUser:
        username="test_user"
    return FakeUser()
