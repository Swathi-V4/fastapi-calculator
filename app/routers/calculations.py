from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import get_current_user


router = APIRouter(
    prefix="/calculations",
    tags=["Calculations"],
)


def calculate_result(
    a: float,
    b: float,
    calculation_type: schemas.CalculationType,
) -> float:
    """
    Calculate the result based on the selected operation.
    """
    if calculation_type == schemas.CalculationType.ADD:
        return a + b

    if calculation_type == schemas.CalculationType.SUBTRACT:
        return a - b

    if calculation_type == schemas.CalculationType.MULTIPLY:
        return a * b

    if calculation_type == schemas.CalculationType.DIVIDE:
        if b == 0:
            raise ValueError("Division by zero is not allowed")

        return a / b

    raise ValueError("Invalid calculation type")


@router.get(
    "/",
    response_model=list[schemas.CalculationRead],
    status_code=status.HTTP_200_OK,
)
def browse_calculations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Return all calculations belonging to the logged-in user.
    """
    return (
        db.query(models.Calculation)
        .filter(models.Calculation.user_id == current_user.id)
        .order_by(models.Calculation.id.desc())
        .all()
    )


@router.get(
    "/{calculation_id}",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_200_OK,
)
def read_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Return one calculation belonging to the logged-in user.
    """
    calculation = (
        db.query(models.Calculation)
        .filter(
            models.Calculation.id == calculation_id,
            models.Calculation.user_id == current_user.id,
        )
        .first()
    )

    if calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    return calculation


@router.post(
    "/",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def add_calculation(
    calculation_data: schemas.CalculationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Create and save a calculation for the logged-in user.
    """
    try:
        result = calculate_result(
            calculation_data.a,
            calculation_data.b,
            calculation_data.type,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    calculation = models.Calculation(
        a=calculation_data.a,
        b=calculation_data.b,
        type=calculation_data.type.value,
        result=result,
        user_id=current_user.id,
    )

    db.add(calculation)
    db.commit()
    db.refresh(calculation)

    return calculation


@router.put(
    "/{calculation_id}",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_200_OK,
)
def edit_calculation(
    calculation_id: int,
    calculation_data: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Update a calculation belonging to the logged-in user.
    """
    calculation = (
        db.query(models.Calculation)
        .filter(
            models.Calculation.id == calculation_id,
            models.Calculation.user_id == current_user.id,
        )
        .first()
    )

    if calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    try:
        result = calculate_result(
            calculation_data.a,
            calculation_data.b,
            calculation_data.type,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    calculation.a = calculation_data.a
    calculation.b = calculation_data.b
    calculation.type = calculation_data.type.value
    calculation.result = result

    db.commit()
    db.refresh(calculation)

    return calculation


@router.delete(
    "/{calculation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Delete a calculation belonging to the logged-in user.
    """
    calculation = (
        db.query(models.Calculation)
        .filter(
            models.Calculation.id == calculation_id,
            models.Calculation.user_id == current_user.id,
        )
        .first()
    )

    if calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    db.delete(calculation)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)