def test_create_task_requires_auth(client):
    r = client.post("/tasks", json={"title": "T1", "description": "D1"})
    assert r.status_code == 401  # precisa de token


def test_crud_task_with_auth(client, user_and_token):
    _, token = user_and_token
    headers = {"Authorization": f"Bearer {token}"}

    # create
    r = client.post(
        "/tasks", json={"title": "Estudar", "description": "JWT"}, headers=headers
    )
    assert r.status_code == 200
    task = r.json()
    task_id = task["id"]
    assert task["completed"] is False

    # list
    r = client.get("/tasks")
    assert r.status_code == 200
    assert any(t["id"] == task_id for t in r.json())

    # update
    r = client.put(
        f"/tasks/{task_id}",
        json={"title": "Estudar muito", "description": "JWT+tests"},
        headers=headers,
    )
    assert r.status_code == 200
    assert r.json()["title"] == "Estudar muito"

    # delete
    r = client.delete(f"/tasks/{task_id}", headers=headers)
    assert r.status_code == 200

    # confirm deletion
    r = client.get("/tasks")
    ids = [t["id"] for t in r.json()]
    assert task_id not in ids
