def test_register_and_login(client):
    # register
    r = client.post("/register", json={"username": "alice", "password": "pwd"})
    assert r.status_code in (200, 400)  # 400 se ja criada

    # login
    r = client.post("/login", json={"username": "alice", "password": "pwd"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    # garante usuario
    client.post("/register", json={"username": "bob", "password": "pwd"})
    # senha errada
    r.client.post("/login", json={"username": "bob", "password": "wrong"})
    assert r.status_code == 401
