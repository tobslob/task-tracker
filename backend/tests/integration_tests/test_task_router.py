from fastapi.testclient import TestClient
from uuid import uuid5, NAMESPACE_DNS


def test_task_crud(client: TestClient):
    # sign in first user to get token
    response = client.post(
        "/api/v1/auth/sign-in",
        json={"email": "test1@test1.com", "password": "test1"},
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    # create task
    response = client.post(
        "/api/v1/task",
        json={
            "title": "New Task",
            "description": "from test",
            "due_date": "2025-01-04",
        },
        headers=headers,
    )
    assert response.status_code == 200
    task = response.json()
    task_id = task["id"]
    assert task["title"] == "New Task"
    assert task["due_date"] == "2025-01-04"

    # get task
    response = client.get(f"/api/v1/task/{task_id}", headers=headers)
    assert response.status_code == 200

    # update task status
    response = client.patch(
        f"/api/v1/task/{task_id}",
        json={"status": "in-progress"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "in-progress"

    # mark task complete using new endpoint
    response = client.post(f"/api/v1/task/{task_id}/complete", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

    # delete task
    response = client.delete(f"/api/v1/task/{task_id}", headers=headers)
    assert response.status_code == 200


def test_task_filter(client: TestClient):
    """Test filtering tasks by user_id using eq operator."""

    # sign in and request tasks belonging to the current user
    response = client.post(
        "/api/v1/auth/sign-in",
        json={"email": "test1@test1.com", "password": "test1"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    user_id = str(uuid5(NAMESPACE_DNS, "test1"))
    response = client.get(
        "/api/v1/task", params={"user_id__eq": user_id}, headers=headers
    )
    assert response.status_code == 200
    founds = response.json()["founds"]
    assert len(founds) == 1
    assert all(task["user_id"] == user_id for task in founds)


def test_task_filter_pagination(client: TestClient):
    """Filtering with pagination options should split results across pages."""

    response = client.post(
        "/api/v1/auth/sign-in",
        json={"email": "test_super@test_super.com", "password": "test_super"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Filter tasks by completion status to get two results
    response = client.get(
        "/api/v1/task",
        params={"status": "pending", "ordering": "id", "page_size": 1, "page": 1},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["search_options"]["total_count"] == 2
    assert len(data["founds"]) == 1
    first_id = data["founds"][0]["id"]

    # second page should return the remaining task
    response = client.get(
        "/api/v1/task",
        params={"status": "pending", "ordering": "id", "page_size": 1, "page": 2},
        headers=headers,
    )
    assert response.status_code == 200
    data2 = response.json()
    assert len(data2["founds"]) == 1
    assert data2["founds"][0]["id"] != first_id
    assert data2["search_options"]["total_count"] == 2


def test_task_search(client: TestClient):
    """Tasks can be searched by title or description."""

    response = client.post(
        "/api/v1/auth/sign-in",
        json={"email": "test1@test1.com", "password": "test1"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/task", params={"search": "task"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    # only tasks belonging to test1 should be returned (1 task)
    assert data["search_options"]["total_count"] == 1
