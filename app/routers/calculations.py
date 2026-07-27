from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(
    prefix="/calculations",
    tags=["Calculations"],
)


@router.get(
    "/",
    response_model=list[schemas.CalculationRead],
    status_code=status.HTTP_200_OK,
)
def browse_calculations(
    db: Session = Depends(get_db),
):
    """
    Browse all saved calculations.
    """
    return crud.get_calculations(db)


@router.get(
    "/{calculation_id}",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_200_OK,
)
def read_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
):
    """
    Read one calculation by its ID.
    """
    calculation = crud.get_calculation(
        db,
        calculation_id,
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
    calculation: schemas.CalculationCreate,
    db: Session = Depends(get_db),
):
    """
    Add and save a new calculation.
    """
    try:
        return crud.create_calculation(
            db,
            calculation,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    "/{calculation_id}",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_200_OK,
)
def edit_calculation(
    calculation_id: int,
    calculation: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
):
    """
    Edit an existing calculation.
    """
    try:
        updated_calculation = crud.update_calculation(
            db,
            calculation_id,
            calculation,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if updated_calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    return updated_calculation


@router.delete(
    "/{calculation_id}",
    status_code=status.HTTP_200_OK,
)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a calculation.
    """
    deleted_calculation = crud.delete_calculation(
        db,
        calculation_id,
    )

    if deleted_calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    return {
        "message": "Calculation deleted successfully",
        "calculation_id": calculation_id,
    }