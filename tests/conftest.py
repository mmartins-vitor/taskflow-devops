import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base
from app import models
from app.auth import get_db as real_get_db  # para referência
from app.database import SessionLocal as RealSessionLocal

# ---- Engine/Session de teste (SQLite em memória)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Cria as tabelas UMA vez por sessão de testes
@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Override do get_db para usar a sessão de teste
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[real_get_db] = override_get_db


# Cliente de testes
@pytest.fixture()
def client():
    return TestClient(app)


# Helper: cria usuário e retorna token
@pytest.fixture()
def user_and_token(client):
    # registra
    r = client.post("/register", json={"username": "vitor", "password": "123456"})
    assert r.status_code in (200, 400)  # 400 se já existir

    # login via /login (JSON) – mais simples no teste
    r = client.post("/login", json={"username": "vitor", "password": "123456"})
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    return ("vitor", token)
