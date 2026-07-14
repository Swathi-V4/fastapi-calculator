import logging

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import Base, engine, get_db
from app.operations import add, divide, multiply, subtract


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


# Create database tables
Base.metadata.create_all(bind=engine)


# Setup templates directory
templates = Jinja2Templates(directory="templates")


# Pydantic model for calculator request data
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator("a", "b")
    @classmethod
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Both a and b must be numbers.")
        return value


# Pydantic model for successful calculator response
class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")


# Pydantic model for error response
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")


# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(
        "HTTPException on %s: %s",
        request.url.path,
        exc.detail,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    error_messages = "; ".join(
        f"{error['loc'][-1]}: {error['msg']}"
        for error in exc.errors()
    )

    logger.error(
        "ValidationError on %s: %s",
        request.url.path,
        error_messages,
    )

    return JSONResponse(
        status_code=400,
        content={"error": error_messages},
    )


@app.get("/")
async def read_root(request: Request):
    """
    Serve the calculator homepage.
    """
    logger.info("Calculator homepage accessed")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.post(
    "/users/",
    response_model=schemas.UserRead,
    status_code=201,
    responses={400: {"model": ErrorResponse}},
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a user while hashing the password before storage.
    """
    try:
        db_user = crud.create_user(db, user)

        logger.info(
            "User created successfully: %s",
            db_user.username,
        )

        return db_user

    except ValueError as exc:
        logger.warning(
            "User creation failed: %s",
            str(exc),
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post(
    "/add",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def add_route(operation: OperationRequest):
    """
    Add two numbers.
    """
    try:
        logger.info(
            "Adding %s and %s",
            operation.a,
            operation.b,
        )

        result = add(operation.a, operation.b)

        logger.info("Addition result: %s", result)

        return OperationResponse(result=result)

    except Exception as exc:
        logger.error("Add Operation Error: %s", str(exc))

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post(
    "/subtract",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def subtract_route(operation: OperationRequest):
    """
    Subtract two numbers.
    """
    try:
        logger.info(
            "Subtracting %s from %s",
            operation.b,
            operation.a,
        )

        result = subtract(operation.a, operation.b)

        logger.info("Subtraction result: %s", result)

        return OperationResponse(result=result)

    except Exception as exc:
        logger.error("Subtract Operation Error: %s", str(exc))

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post(
    "/multiply",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def multiply_route(operation: OperationRequest):
    """
    Multiply two numbers.
    """
    try:
        logger.info(
            "Multiplying %s and %s",
            operation.a,
            operation.b,
        )

        result = multiply(operation.a, operation.b)

        logger.info("Multiplication result: %s", result)

        return OperationResponse(result=result)

    except Exception as exc:
        logger.error("Multiply Operation Error: %s", str(exc))

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post(
    "/divide",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def divide_route(operation: OperationRequest):
    """
    Divide two numbers.
    """
    try:
        logger.info(
            "Dividing %s by %s",
            operation.a,
            operation.b,
        )

        result = divide(operation.a, operation.b)

        logger.info("Division result: %s", result)

        return OperationResponse(result=result)

    except ValueError as exc:
        logger.error("Divide Operation Error: %s", str(exc))

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.error(
            "Divide Operation Internal Error: %s",
            str(exc),
        )

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        ) from exc


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )