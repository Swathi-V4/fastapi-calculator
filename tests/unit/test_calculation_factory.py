import pytest

from app.schemas import CalculationType
from app.services.calculation_factory import CalculationFactory


@pytest.mark.parametrize(
    "calculation_type,a,b,expected",
    [
        (CalculationType.ADD, 10, 5, 15),
        (CalculationType.SUBTRACT, 10, 5, 5),
        (CalculationType.MULTIPLY, 10, 5, 50),
        (CalculationType.DIVIDE, 10, 5, 2),
    ],
)
def test_factory_calculates_correct_result(
    calculation_type,
    a,
    b,
    expected,
):
    result = CalculationFactory.calculate(
        calculation_type,
        a,
        b,
    )

    assert result == expected


def test_factory_rejects_division_by_zero():
    with pytest.raises(
        ValueError,
        match="Division by zero is not allowed",
    ):
        CalculationFactory.calculate(
            CalculationType.DIVIDE,
            10,
            0,
        )


def test_factory_rejects_invalid_operation():
    with pytest.raises(
        ValueError,
        match="Unsupported calculation type",
    ):
        CalculationFactory.create("Power")