import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.security import create_access_token, verify_password


logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    """Register a new user and securely hash the password."""
    try:
        db_user = crud.create_user(db, user)

        logger.info(
            "User registered successfully: %s",
            db_user.username,
        )

        return db_user

    except ValueError as exc:
        logger.warning(
            "Registration failed: %s",
            str(exc),
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/login",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK,
)
def login_user(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    """Authenticate a user and return a JWT access token."""
    db_user = crud.get_user_by_email(
        db,
        credentials.email,
    )

    if db_user is None or not verify_password(
        credentials.password,
        db_user.password_hash,
    ):
        logger.warning(
            "Login failed for email: %s",
            credentials.email,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={
            "sub": str(db_user.id),
            "email": db_user.email,
            "username": db_user.username,
        }
    )

    logger.info(
        "User logged in successfully: %s",
        db_user.username,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }