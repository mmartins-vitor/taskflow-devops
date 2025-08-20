# tests/conftest.py serve para a configuração do ambiente de teste
import os

# 1) Força SQLite em memória ANTES dos imports da app
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine, SessionLocal
from app import (
    models,
)  # << garante que as tabelas (User/Task) estejam registradas no Base
from app.main import app
from app.auth import get_db as real_get_db


# 2) Cria/Derruba tabelas usando o MESMO engine da app (que agora é :memory: + StaticPool)
@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# 3) Override do get_db para usar a SessionLocal ligada ao mesmo engine acima
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[real_get_db] = override_get_db


# 4) Client de testes
@pytest.fixture()
def client():
    return TestClient(app)


# 5) Helper: cria usuário e retorna token
@pytest.fixture()
def user_and_token(client):
    client.post("/register", json={"username": "vitor", "password": "123456"})
    r = client.post("/login", json={"username": "vitor", "password": "123456"})
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    return ("vitor", token)
