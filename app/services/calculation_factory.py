from abc import ABC, abstractmethod

from app.schemas import CalculationType


class CalculationOperation(ABC):
    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        pass


class AddOperation(CalculationOperation):
    def calculate(self, a: float, b: float) -> float:
        return a + b


class SubtractOperation(CalculationOperation):
    def calculate(self, a: float, b: float) -> float:
        return a - b


class MultiplyOperation(CalculationOperation):
    def calculate(self, a: float, b: float) -> float:
        return a * b


class DivideOperation(CalculationOperation):
    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed")

        return a / b


class CalculationFactory:
    _operations = {
        CalculationType.ADD: AddOperation,
        CalculationType.SUBTRACT: SubtractOperation,
        CalculationType.MULTIPLY: MultiplyOperation,
        CalculationType.DIVIDE: DivideOperation,
    }

    @classmethod
    def create(cls, calculation_type: CalculationType) -> CalculationOperation:
        operation_class = cls._operations.get(calculation_type)

        if operation_class is None:
            raise ValueError(
                f"Unsupported calculation type: {calculation_type}"
            )

        return operation_class()

    @classmethod
    def calculate(
        cls,
        calculation_type: CalculationType,
        a: float,
        b: float,
    ) -> float:
        operation = cls.create(calculation_type)
        return operation.calculate(a, b)