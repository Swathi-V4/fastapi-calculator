from app.security import hash_password, verify_password


def test_hash_password_does_not_store_plain_text():
    plain_password = "Password123"

    hashed_password = hash_password(plain_password)

    assert hashed_password != plain_password
    assert isinstance(hashed_password, str)


def test_verify_password_returns_true_for_correct_password():
    plain_password = "Password123"

    hashed_password = hash_password(plain_password)

    assert verify_password(plain_password, hashed_password) is True


def test_verify_password_returns_false_for_incorrect_password():
    hashed_password = hash_password("Password123")

    assert verify_password("WrongPassword", hashed_password) is False


def test_same_password_produces_different_hashes():
    plain_password = "Password123"

    first_hash = hash_password(plain_password)
    second_hash = hash_password(plain_password)

    assert first_hash != second_hash