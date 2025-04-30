import pytest
from sqlmodel import create_engine, SQLModel
from sqlmodel import Session
from fastapi import TestClient
from app.main import app
from app.db.session import get_session

DB_URL = 'sqlite:///./test.db'
engine = create_engine(DB_URL)

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture
def client():
    return TestClient(app)