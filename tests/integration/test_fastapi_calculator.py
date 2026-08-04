import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_add_api(client):
    response = client.post(
        "/add",
        json={"a": 10, "b": 5},
    )

    assert response.status_code == 200
    assert response.json()["result"] == 15


def test_subtract_api(client):
    response = client.post(
        "/subtract",
        json={"a": 10, "b": 5},
    )

    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_multiply_api(client):
    response = client.post(
        "/multiply",
        json={"a": 10, "b": 5},
    )

    assert response.status_code == 200
    assert response.json()["result"] == 50


def test_divide_api(client):
    response = client.post(
        "/divide",
        json={"a": 10, "b": 2},
    )

    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_divide_by_zero_api(client):
    response = client.post(
        "/divide",
        json={"a": 10, "b": 0},
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Cannot divide by zero!"


def test_invalid_operand_api(client):
    response = client.post(
        "/add",
        json={"a": "not-a-number", "b": 5},
    )

    assert response.status_code == 400
    assert "error" in response.json()