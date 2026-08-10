from datetime import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


# -------------------------
# User schemas
# -------------------------

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -------------------------
# Calculation schemas
# -------------------------

class CalculationType(str, Enum):
    ADD = "Add"
    SUBTRACT = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"
    POWER = "Power"


class CalculationCreate(BaseModel):
    a: float = Field(allow_inf_nan=False)
    b: float = Field(allow_inf_nan=False)
    type: CalculationType

    @model_validator(mode="after")
    def validate_division(self):
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Division by zero is not allowed")

        return self


class CalculationUpdate(BaseModel):
    a: float = Field(allow_inf_nan=False)
    b: float = Field(allow_inf_nan=False)
    type: CalculationType

    @model_validator(mode="after")
    def validate_division(self):
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Division by zero is not allowed")

        return self


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    result: float
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)