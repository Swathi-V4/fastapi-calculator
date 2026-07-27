# FastAPI Calculator

A FastAPI application that supports secure user registration and login using JWT authentication, along with CRUD operations for calculations using PostgreSQL, SQLAlchemy, and Pydantic.

## Running the Application

Clone the repository:

```bash
git clone https://github.com/Swathi-V4/fastapi-calculator.git
cd fastapi-calculator
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

### Mac/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application with Docker:

```bash
docker compose up --build
```

The application will be available at:

- Application: http://localhost:8000
- OpenAPI Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

## Front-End Pages

After the application is running, open your browser and visit:

- Registration Page: http://localhost:8000/register-page
- Login Page: http://localhost:8000/login-page

---

## Running Tests Locally

Run all unit and integration tests:

```bash
pytest tests/unit tests/integration -v
```

Run tests with coverage:

```bash
pytest tests/unit tests/integration --cov=app
```

Run only unit tests:

```bash
pytest tests/unit -v
```

Run only integration tests:

```bash
pytest tests/integration -v
```

## Running Playwright E2E Tests

Install the Playwright browser:

```bash
python -m playwright install chromium
```

Run the Playwright end-to-end tests:

```bash
pytest tests/test_auth_e2e.py -v --no-cov
```

---

## Manual Testing

Open the OpenAPI documentation at:

```
http://localhost:8000/docs
```

Verify the following endpoints:

- Register User
- Login User
- Browse Calculations
- Add Calculation
- Read Calculation
- Edit Calculation
- Delete Calculation

You can also verify the front-end pages:

- http://localhost:8000/register-page
- http://localhost:8000/login-page

---

## Docker Hub Repository

https://hub.docker.com/r/swathi638/fastapi-calculator