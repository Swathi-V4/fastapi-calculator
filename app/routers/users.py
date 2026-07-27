import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.security import verify_password


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
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
    """
    Register a new user and securely hash the password.
    """
    try:
        db_user = crud.create_user(
            db,
            user,
        )

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
    status_code=status.HTTP_200_OK,
)
def login_user(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    """
    Verify a user's username and hashed password.
    """
    db_user = crud.get_user_by_username(
        db,
        credentials.username,
    )

    if db_user is None or not verify_password(
        credentials.password,
        db_user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    logger.info(
        "User logged in successfully: %s",
        db_user.username,
    )

    return {
        "message": "Login successful",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
        },
    }