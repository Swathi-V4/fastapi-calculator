import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import models
from app.database import get_db


# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# JWT configuration
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "your-secret-key-change-this",
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI reads the token from:
# Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password before storing it.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify that a plain-text password matches its hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_token(token: str) -> dict | None:
    """
    Decode and verify a JWT token.
    """
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except JWTError:
        return None


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    """
    Return the user represented by the JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)

    if payload is None:
        raise credentials_exception

    subject = payload.get("sub")

    if subject is None:
        raise credentials_exception

    user = None

    # Supports tokens whose subject contains a user ID.
    try:
        user_id = int(subject)

        user = (
            db.query(models.User)
            .filter(models.User.id == user_id)
            .first()
        )
    except (TypeError, ValueError):
        pass

    # Also supports tokens whose subject contains an email
    # or username.
    if user is None:
        user = (
            db.query(models.User)
            .filter(
                (models.User.email == subject)
                | (models.User.username == subject)
            )
            .first()
        )

    if user is None:
        raise credentials_exception

    return user