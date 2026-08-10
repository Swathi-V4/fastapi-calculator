# FastAPI Calculator

A full-stack FastAPI calculator application that supports secure user authentication and complete BREAD (Browse, Read, Edit, Add, Delete) operations for user calculations. The application uses PostgreSQL for data storage, SQLAlchemy as the ORM, JWT authentication for security, Docker for containerization, Playwright for end-to-end testing, and GitHub Actions for continuous integration and deployment.

---

## Features

- User registration and login with JWT authentication
- Password hashing using bcrypt
- PostgreSQL database with SQLAlchemy ORM
- Complete BREAD operations for calculations
- Addition, subtraction, multiplication, division, and power calculations
- User-specific calculation history
- User authorization and ownership protection
- Client-side and server-side validation
- Division-by-zero validation
- Unit and integration testing with pytest
- End-to-end testing with Playwright
- Dockerized application
- GitHub Actions CI/CD workflow

---

## Technologies Used

- Python 3.10
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- Passlib (bcrypt)
- Docker
- Docker Compose
- Playwright
- Pytest
- GitHub Actions

---

## Project Structure

```text
fastapi-calculator/
│
├── app/
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── services/
│   └── routers/
│
├── templates/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
└── README.md
```

---

# Running the Application

## 1. Clone the Repository

```bash
git clone https://github.com/Swathi-V4/fastapi-calculator.git
cd fastapi-calculator
```

## 2. Build and Start the Application

Make sure Docker Desktop is running, then execute:

```bash
docker compose up -d --build
```

The FastAPI application will be available at:

```text
http://localhost:8000
```

## 3. Stop the Application

```bash
docker compose down
```

---

# Running Tests Locally

Make sure Docker Desktop is running and start the application first:

```bash
docker compose up -d
```

## Run Unit and Integration Tests

```bash
docker compose run --rm web pytest tests/unit tests/integration -v
```

These tests verify the application logic, schemas, authentication, database integration, calculation operations, and BREAD API routes.

## Run Playwright End-to-End Tests

```bash
docker compose run --rm -e BASE_URL=http://web:8000 web pytest tests/e2e -v
```

The Playwright tests verify the application through the browser, including registration, login, calculation operations, invalid login handling, power calculations, and division-by-zero validation.

---

# API Endpoints

## Authentication

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| POST | `/register` | Register a new user |
| POST | `/login` | Login and receive a JWT token |

## Calculations

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | `/calculations/` | Browse calculations for the logged-in user |
| GET | `/calculations/{id}` | Read a specific calculation |
| POST | `/calculations/` | Add a new calculation |
| PUT | `/calculations/{id}` | Edit an existing calculation |
| DELETE | `/calculations/{id}` | Delete a calculation |

---

# Testing

The project includes:

- Unit tests
- Integration tests
- Playwright end-to-end tests

The automated tests verify:

- User registration and login
- JWT authentication
- Password hashing
- Calculation BREAD operations
- Addition, subtraction, multiplication, division, and power operations
- Database persistence
- Input validation
- Division-by-zero handling
- Invalid operation handling
- User authorization and ownership protection

The completed unit and integration test suite contains 60 passing tests. The Playwright E2E suite contains 4 passing tests.

---

# Continuous Integration and Deployment

GitHub Actions is used to automate the CI/CD workflow. The pipeline:

- Installs project dependencies
- Starts PostgreSQL
- Runs automated tests
- Supports Playwright end-to-end testing
- Builds the Docker image
- Pushes the application image to Docker Hub

---

# Docker Hub

The Docker image for this project is available at:

https://hub.docker.com/r/swathi638/fastapi-calculator

---
# Reflection

This final project strengthened my understanding of how different parts of a full-stack application work together. I expanded the calculator by adding exponentiation as a new calculation type and integrated it throughout the backend, front end, validation, and testing. One of the most important parts of this project was making sure the new feature worked without breaking the existing BREAD operations or authentication system.

Testing was especially helpful because unit, integration, and Playwright end-to-end tests verified the application at different levels. I also gained more experience troubleshooting Docker and Playwright issues, particularly when the E2E tests initially could not connect to the FastAPI server. After resolving these issues, all of the tests passed successfully.

Finally, using GitHub Actions and Docker Hub helped me understand how automated testing and deployment fit into a professional development workflow. Overall, this project improved my confidence with FastAPI, SQLAlchemy, Pydantic, Docker, automated testing, and CI/CD.
---

# Author

**Swathi Veerapalli**