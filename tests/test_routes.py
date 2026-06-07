# tests/test_routes.py
# pytest finds functions starting with "test_" and runs them.
# Each test should check ONE specific behaviour of our app.

import pytest
from app import create_app
from app import models


@pytest.fixture(autouse=True)
def reset_todos():
    """Before every test, wipe the todos list clean.
    This stops tests from interfering with each other.
    """
    models.todos.clear()
    models.next_id = 1


@pytest.fixture
def client():
    """Create a test version of our Flask app.
    'testing=True' gives us better error messages in tests.
    """
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """The /health endpoint should always return 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_get_todos_empty(client):
    """When no todos exist, we should get an empty list."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_todo(client):
    """Creating a todo should return it with id=1 and done=False."""
    response = client.post("/todos", json={"title": "Learn Docker"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 1
    assert data["title"] == "Learn Docker"
    assert data["done"] is False


def test_create_todo_missing_title(client):
    """Sending no title should return a 400 Bad Request."""
    response = client.post("/todos", json={})
    assert response.status_code == 400


def test_update_todo(client):
    """We should be able to mark a todo as done."""
    client.post("/todos", json={"title": "Learn Docker"})
    response = client.patch("/todos/1", json={"done": True})
    assert response.status_code == 200
    assert response.get_json()["done"] is True


def test_delete_todo(client):
    """Deleting a todo should remove it from the list."""
    client.post("/todos", json={"title": "Learn Docker"})
    response = client.delete("/todos/1")
    assert response.status_code == 200
    # Confirm it's really gone
    assert client.get("/todos").get_json() == []


def test_delete_nonexistent_todo(client):
    """Deleting a todo that doesn't exist should return 404."""
    response = client.delete("/todos/999")
    assert response.status_code == 404