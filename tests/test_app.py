import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from models import User, Task
import pytest


@pytest.fixture
def client():
    """Setup test client with in-memory database"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def register_user(client, username="testuser", password="password"):
    return client.post("/auth/register", json={
        "username": username,
        "password": password
    })


def login_user(client, username="testuser", password="password"):
    return client.post("/auth/login", json={
        "username": username,
        "password": password
    })


def test_register_and_login(client):
    """Test user registration and login"""
    res = register_user(client)
    assert res.status_code == 201 or res.status_code == 200

    res = login_user(client)
    assert res.status_code == 200
    assert "access_token" in res.get_json()


def test_create_task(client):
    """Test creating a task with JWT"""
    register_user(client)
    login_res = login_user(client)
    token = login_res.get_json()["access_token"]

    res = client.post("/tasks", json={"title": "Test Task"}, headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 201 or res.status_code == 200
    data = res.get_json()
    assert "title" in data
    assert data["title"] == "Test Task"


def test_get_tasks(client):
    """Test listing tasks"""
    register_user(client)
    login_res = login_user(client)
    token = login_res.get_json()["access_token"]

    client.post("/tasks", json={"title": "Task 1"}, headers={
        "Authorization": f"Bearer {token}"
    })

    res = client.get("/tasks")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, dict)
    assert "items" in data
    assert len(data["items"]) >= 1


def test_unauthorized_access(client):
    """Test access to protected route without JWT"""
    res = client.post("/tasks", json={"title": "Task 1"})
    assert res.status_code == 401 or res.status_code == 422

