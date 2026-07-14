from sqlalchemy.orm import Session

from app import models, schemas
from app.security import hash_password


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    # Check for duplicate username
    if get_user_by_username(db, user.username):
        raise ValueError("Username already exists")

    # Check for duplicate email
    if get_user_by_email(db, user.email):
        raise ValueError("Email already exists")

    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user