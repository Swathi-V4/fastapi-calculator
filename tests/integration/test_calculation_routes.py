from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, engine
from app.models import Calculation, User
from main import app


client = TestClient(app)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def registered_user():
    unique_value = uuid4().hex[:8]

    user_data = {
        "username": f"calcuser_{unique_value}",
        "email": f"calcuser_{unique_value}@example.com",
        "password": "SecurePassword123",
    }

    register_response = client.post(
        "/register",
        json=user_data,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/login",
        json={
            "email": user_data["email"],
            "password": user_data["password"],
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "user_data": user_data,
        "token": token,
        "headers": {
            "Authorization": f"Bearer {token}",
        },
    }


@pytest.fixture(autouse=True)
def clean_calculation_test_data():
    yield

    db = SessionLocal()

    try:
        test_users = (
            db.query(User)
            .filter(User.username.like("calcuser_%"))
            .all()
        )

        user_ids = [user.id for user in test_users]

        if user_ids:
            db.query(Calculation).filter(
                Calculation.user_id.in_(user_ids)
            ).delete(synchronize_session=False)

            db.query(User).filter(
                User.id.in_(user_ids)
            ).delete(synchronize_session=False)

        db.commit()
    finally:
        db.close()


def test_unauthorized_calculation_access():
    response = client.get("/calculations/")

    assert response.status_code == 401


def test_add_and_browse_calculation(registered_user):
    create_response = client.post(
        "/calculations/",
        headers=registered_user["headers"],
        json={
            "a": 10,
            "b": 5,
            "type": "Add",
        },
    )

    assert create_response.status_code == 201

    created = create_response.json()

    assert created["a"] == 10
    assert created["b"] == 5
    assert created["type"] == "Add"
    assert created["result"] == 15
    assert "user_id" in created

    browse_response = client.get(
        "/calculations/",
        headers=registered_user["headers"],
    )

    assert browse_response.status_code == 200

    calculations = browse_response.json()

    assert len(calculations) == 1
    assert calculations[0]["id"] == created["id"]


def test_power_calculation(registered_user):
    """
    Verify that a Power calculation is processed by the API,
    stored in the database, and can be retrieved successfully.
    """
    create_response = client.post(
        "/calculations/",
        headers=registered_user["headers"],
        json={
            "a": 2,
            "b": 5,
            "type": "Power",
        },
    )

    assert create_response.status_code == 201

    created = create_response.json()

    assert created["a"] == 2
    assert created["b"] == 5
    assert created["type"] == "Power"
    assert created["result"] == 32

    calculation_id = created["id"]

    read_response = client.get(
        f"/calculations/{calculation_id}",
        headers=registered_user["headers"],
    )

    assert read_response.status_code == 200

    saved = read_response.json()

    assert saved["id"] == calculation_id
    assert saved["type"] == "Power"
    assert saved["result"] == 32


def test_read_calculation(registered_user):
    create_response = client.post(
        "/calculations/",
        headers=registered_user["headers"],
        json={
            "a": 20,
            "b": 4,
            "type": "Divide",
        },
    )

    calculation_id = create_response.json()["id"]

    read_response = client.get(
        f"/calculations/{calculation_id}",
        headers=registered_user["headers"],
    )

    assert read_response.status_code == 200
    assert read_response.json()["result"] == 5


def test_edit_calculation(registered_user):
    create_response = client.post(
        "/calculations/",
        headers=registered_user["headers"],
        json={
            "a": 5,
            "b": 3,
            "type": "Add",
        },
    )

    calculation_id = create_response.json()["id"]

    update_response = client.put(
        f"/calculations/{calculation_id}",
        headers=registered_user["headers"],
        json={
            "a": 5,
            "b": 3,
            "type": "Multiply",
        },
    )

    assert update_response.status_code == 200

    updated = update_response.json()

    assert updated["type"] == "Multiply"
    assert updated["result"] == 15


def test_delete_calculation(registered_user):
    create_response = client.post(
        "/calculations/",
        headers=registered_user["headers"],
        json={
            "a": 9,
            "b": 3,
            "type": "Sub",
        },
    )

    calculation_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/calculations/{calculation_id}",
        headers=registered_user["headers"],
    )

    assert delete_response.status_code == 204

    read_response = client.get(
        f"/calculations/{calculation_id}",
        headers=registered_user["headers"],
    )

    assert read_response.status_code == 404


def test_division_by_zero_is_rejected(registered_user):
    response = client.post(
        "/calculations/",
        headers=registered_user["headers"],
        json={
            "a": 10,
            "b": 0,
            "type": "Divide",
        },
    )

    assert response.status_code == 400
    assert "Division by zero" in response.json()["error"]


def test_user_cannot_read_another_users_calculation():
    first_user = create_registered_user()
    second_user = create_registered_user()

    create_response = client.post(
        "/calculations/",
        headers=first_user["headers"],
        json={
            "a": 12,
            "b": 3,
            "type": "Divide",
        },
    )

    calculation_id = create_response.json()["id"]

    response = client.get(
        f"/calculations/{calculation_id}",
        headers=second_user["headers"],
    )

    assert response.status_code == 404


def create_registered_user():
    unique_value = uuid4().hex[:8]

    user_data = {
        "username": f"calcuser_{unique_value}",
        "email": f"calcuser_{unique_value}@example.com",
        "password": "SecurePassword123",
    }

    register_response = client.post(
        "/register",
        json=user_data,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/login",
        json={
            "email": user_data["email"],
            "password": user_data["password"],
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "headers": {
            "Authorization": f"Bearer {token}",
        }
    }