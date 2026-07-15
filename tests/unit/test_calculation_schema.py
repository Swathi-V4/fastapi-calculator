import pytest
from pydantic import ValidationError

from app.schemas import CalculationCreate, CalculationType


def test_calculation_create_accepts_valid_input():
    calculation = CalculationCreate(
        a=10,
        b=5,
        type="Add",
    )

    assert calculation.a == 10
    assert calculation.b == 5
    assert calculation.type == CalculationType.ADD


def test_calculation_create_rejects_invalid_type():
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10,
            b=5,
            type="Power",
        )


def test_calculation_create_rejects_zero_division():
    with pytest.raises(
        ValidationError,
        match="Division by zero is not allowed",
    ):
        CalculationCreate(
            a=10,
            b=0,
            type="Divide",
        )


def test_calculation_create_accepts_subtraction():
    calculation = CalculationCreate(
        a=20,
        b=8,
        type="Sub",
    )

    assert calculation.type == CalculationType.SUBTRACT