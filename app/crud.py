from sqlalchemy.orm import Session

from app import models, schemas
from app.security import hash_password
from app.services.calculation_factory import CalculationFactory


# -------------------------
# User CRUD
# -------------------------

def get_user_by_username(
    db: Session,
    username: str,
):
    return (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )


def get_user_by_email(
    db: Session,
    email: str,
):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


def create_user(
    db: Session,
    user: schemas.UserCreate,
):
    if get_user_by_username(db, user.username):
        raise ValueError("Username already exists")

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


# -------------------------
# Calculation CRUD
# -------------------------

def get_calculations(
    db: Session,
    user_id: int,
):
    """
    Return all calculations owned by a specific user.
    """
    return (
        db.query(models.Calculation)
        .filter(models.Calculation.user_id == user_id)
        .order_by(models.Calculation.id.desc())
        .all()
    )


def get_calculation(
    db: Session,
    calculation_id: int,
    user_id: int,
):
    """
    Return one calculation only when it belongs to the user.
    """
    return (
        db.query(models.Calculation)
        .filter(
            models.Calculation.id == calculation_id,
            models.Calculation.user_id == user_id,
        )
        .first()
    )


def create_calculation(
    db: Session,
    calculation: schemas.CalculationCreate,
    user_id: int,
):
    """
    Create a calculation associated with a specific user.
    """
    result = CalculationFactory.calculate(
        calculation.type,
        calculation.a,
        calculation.b,
    )

    db_calculation = models.Calculation(
        a=calculation.a,
        b=calculation.b,
        type=calculation.type.value,
        result=result,
        user_id=user_id,
    )

    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)

    return db_calculation


def update_calculation(
    db: Session,
    calculation_id: int,
    calculation: schemas.CalculationUpdate,
    user_id: int,
):
    """
    Update a calculation only when it belongs to the user.
    """
    db_calculation = get_calculation(
        db,
        calculation_id,
        user_id,
    )

    if db_calculation is None:
        return None

    result = CalculationFactory.calculate(
        calculation.type,
        calculation.a,
        calculation.b,
    )

    db_calculation.a = calculation.a
    db_calculation.b = calculation.b
    db_calculation.type = calculation.type.value
    db_calculation.result = result

    db.commit()
    db.refresh(db_calculation)

    return db_calculation


def delete_calculation(
    db: Session,
    calculation_id: int,
    user_id: int,
):
    """
    Delete a calculation only when it belongs to the user.
    """
    db_calculation = get_calculation(
        db,
        calculation_id,
        user_id,
    )

    if db_calculation is None:
        return None

    db.delete(db_calculation)
    db.commit()

    return db_calculation