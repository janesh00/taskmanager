import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db

# Use an in-memory SQLite DB for tests
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def registered_user(client):
    client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
    })
    return {"username": "testuser", "password": "testpassword123"}


@pytest.fixture
def auth_headers(client, registered_user):
    resp = client.post("/login", json=registered_user)
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ── Auth Tests ────────────────────────────────────────────────────────────────

class TestAuth:
    def test_register_success(self, client):
        resp = client.post("/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["username"] == "newuser"
        assert "id" in data

    def test_register_duplicate_username(self, client, registered_user):
        resp = client.post("/register", json={
            "username": "testuser",
            "email": "other@example.com",
            "password": "password123",
        })
        assert resp.status_code == 400
        assert "Username already registered" in resp.json()["detail"]

    def test_register_duplicate_email(self, client, registered_user):
        resp = client.post("/register", json={
            "username": "otheruser",
            "email": "test@example.com",
            "password": "password123",
        })
        assert resp.status_code == 400
        assert "Email already registered" in resp.json()["detail"]

    def test_login_success(self, client, registered_user):
        resp = client.post("/login", json=registered_user)
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, registered_user):
        resp = client.post("/login", json={
            "username": "testuser",
            "password": "wrongpassword",
        })
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = client.post("/login", json={
            "username": "nobody",
            "password": "password",
        })
        assert resp.status_code == 401


# ── Task Tests ────────────────────────────────────────────────────────────────

class TestTasks:
    def test_create_task(self, client, auth_headers):
        resp = client.post("/tasks", json={
            "title": "Buy groceries",
            "description": "Milk, bread, eggs",
        }, headers=auth_headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Buy groceries"
        assert data["completed"] is False

    def test_create_task_unauthenticated(self, client):
        resp = client.post("/tasks", json={"title": "Test"})
        assert resp.status_code == 401

    def test_list_tasks(self, client, auth_headers):
        client.post("/tasks", json={"title": "Task 1"}, headers=auth_headers)
        client.post("/tasks", json={"title": "Task 2"}, headers=auth_headers)
        resp = client.get("/tasks", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert len(data["tasks"]) == 2

    def test_list_tasks_filter_completed(self, client, auth_headers):
        resp1 = client.post("/tasks", json={"title": "Task 1"}, headers=auth_headers)
        task_id = resp1.json()["id"]
        client.post("/tasks", json={"title": "Task 2"}, headers=auth_headers)
        client.put(f"/tasks/{task_id}", json={"completed": True}, headers=auth_headers)

        resp = client.get("/tasks?completed=true", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

        resp2 = client.get("/tasks?completed=false", headers=auth_headers)
        assert resp2.json()["total"] == 1

    def test_get_task(self, client, auth_headers):
        created = client.post("/tasks", json={"title": "My Task"}, headers=auth_headers).json()
        resp = client.get(f"/tasks/{created['id']}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["title"] == "My Task"

    def test_get_task_not_found(self, client, auth_headers):
        resp = client.get("/tasks/9999", headers=auth_headers)
        assert resp.status_code == 404

    def test_update_task(self, client, auth_headers):
        created = client.post("/tasks", json={"title": "Old Title"}, headers=auth_headers).json()
        resp = client.put(f"/tasks/{created['id']}", json={
            "title": "New Title",
            "completed": True,
        }, headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "New Title"
        assert data["completed"] is True

    def test_delete_task(self, client, auth_headers):
        created = client.post("/tasks", json={"title": "To Delete"}, headers=auth_headers).json()
        resp = client.delete(f"/tasks/{created['id']}", headers=auth_headers)
        assert resp.status_code == 204

        resp2 = client.get(f"/tasks/{created['id']}", headers=auth_headers)
        assert resp2.status_code == 404

    def test_user_cannot_access_other_users_tasks(self, client, auth_headers):
        # Create task as user1
        created = client.post("/tasks", json={"title": "Private"}, headers=auth_headers).json()

        # Register and login as user2
        client.post("/register", json={
            "username": "user2", "email": "u2@test.com", "password": "pass123"
        })
        token2 = client.post("/login", json={"username": "user2", "password": "pass123"}).json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}

        resp = client.get(f"/tasks/{created['id']}", headers=headers2)
        assert resp.status_code == 404

    def test_pagination(self, client, auth_headers):
        for i in range(15):
            client.post("/tasks", json={"title": f"Task {i}"}, headers=auth_headers)

        resp = client.get("/tasks?page=1&page_size=10", headers=auth_headers)
        data = resp.json()
        assert data["total"] == 15
        assert len(data["tasks"]) == 10

        resp2 = client.get("/tasks?page=2&page_size=10", headers=auth_headers)
        assert len(resp2.json()["tasks"]) == 5
