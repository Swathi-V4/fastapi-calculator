from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, engine
from app.models import User
from app.security import verify_password
from main import app


client = TestClient(app)

# Ensure the database tables exist before testing.
Base.metadata.create_all(bind=engine)


@pytest.fixture
def unique_user_data():
    unique_value = uuid4().hex[:8]

    return {
        "username": f"user_{unique_value}",
        "email": f"user_{unique_value}@example.com",
        "password": "SecurePassword123",
    }


@pytest.fixture(autouse=True)
def clean_test_users():
    """
    Remove users created by integration tests after each test.
    """
    yield

    db = SessionLocal()

    try:
        db.query(User).filter(
            User.username.like("user_%")
        ).delete(synchronize_session=False)

        db.query(User).filter(
            User.email.like("duplicate_%@example.com")
        ).delete(synchronize_session=False)

        db.commit()
    finally:
        db.close()


def test_create_user_in_postgres(unique_user_data):
    response = client.post(
        "/users/",
        json=unique_user_data,
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["username"] == unique_user_data["username"]
    assert response_data["email"] == unique_user_data["email"]
    assert "id" in response_data
    assert "created_at" in response_data
    assert "password" not in response_data
    assert "password_hash" not in response_data


def test_password_is_hashed_in_database(unique_user_data):
    response = client.post(
        "/users/",
        json=unique_user_data,
    )

    assert response.status_code == 201

    db = SessionLocal()

    try:
        saved_user = (
            db.query(User)
            .filter(User.username == unique_user_data["username"])
            .first()
        )

        assert saved_user is not None
        assert saved_user.password_hash != unique_user_data["password"]
        assert verify_password(
            unique_user_data["password"],
            saved_user.password_hash,
        )
    finally:
        db.close()


def test_duplicate_username_is_rejected(unique_user_data):
    first_response = client.post(
        "/users/",
        json=unique_user_data,
    )

    assert first_response.status_code == 201

    duplicate_data = {
        "username": unique_user_data["username"],
        "email": f"duplicate_{uuid4().hex[:8]}@example.com",
        "password": "AnotherPassword123",
    }

    second_response = client.post(
        "/users/",
        json=duplicate_data,
    )

    assert second_response.status_code == 400
    assert second_response.json()["error"] == "Username already exists"


def test_duplicate_email_is_rejected(unique_user_data):
    first_response = client.post(
        "/users/",
        json=unique_user_data,
    )

    assert first_response.status_code == 201

    duplicate_data = {
        "username": f"user_{uuid4().hex[:8]}",
        "email": unique_user_data["email"],
        "password": "AnotherPassword123",
    }

    second_response = client.post(
        "/users/",
        json=duplicate_data,
    )

    assert second_response.status_code == 400
    assert second_response.json()["error"] == "Email already exists"


def test_invalid_email_is_rejected():
    response = client.post(
        "/users/",
        json={
            "username": f"user_{uuid4().hex[:8]}",
            "email": "not-an-email",
            "password": "SecurePassword123",
        },
    )

    assert response.status_code == 400
    assert "email" in response.json()["error"].lower()