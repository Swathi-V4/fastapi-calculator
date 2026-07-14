from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas import UserCreate, UserRead


def test_user_create_accepts_valid_data():
    user = UserCreate(
        username="swathi",
        email="swathi@example.com",
        password="Password123",
    )

    assert user.username == "swathi"
    assert user.email == "swathi@example.com"
    assert user.password == "Password123"


def test_user_create_rejects_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            username="swathi",
            email="not-an-email",
            password="Password123",
        )


def test_user_create_requires_password():
    with pytest.raises(ValidationError):
        UserCreate(
            username="swathi",
            email="swathi@example.com",
        )


def test_user_read_does_not_include_password_hash():
    user = UserRead(
        id=1,
        username="swathi",
        email="swathi@example.com",
        created_at=datetime.now(),
    )

    user_data = user.model_dump()

    assert "password" not in user_data
    assert "password_hash" not in user_data
    assert user_data["username"] == "swathi"