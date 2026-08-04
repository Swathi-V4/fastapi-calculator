# FastAPI Calculator

A full-stack FastAPI calculator application that supports secure user authentication and complete BREAD (Browse, Read, Edit, Add, Delete) operations for user calculations. The application uses PostgreSQL for data storage, SQLAlchemy as the ORM, JWT authentication for security, Docker for containerization, Playwright for end-to-end testing, and GitHub Actions for continuous integration.

---

## Features

- User registration and login with JWT authentication
- Password hashing using bcrypt
- PostgreSQL database with SQLAlchemy ORM
- Complete BREAD operations for calculations
- User-specific calculation history
- Client-side validation
- Integration testing with pytest
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

```
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

## Clone the repository

```bash
git clone https://github.com/Swathi-V4/fastapi-calculator.git
cd fastapi-calculator
```

## Build and start the application

```bash
docker compose up --build
```

The application will be available at:

```
http://localhost:8000
```

## Stop the application

```bash
docker compose down
```

---

# Running Tests

## Run all tests

```bash
pytest
```

## Run integration tests

```bash
pytest tests/integration -v
```

## Run Playwright end-to-end tests

```bash
pytest tests/e2e -v
```

---

# API Endpoints

## Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and receive a JWT token |

## Calculations

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/calculations` | Browse all calculations for the logged-in user |
| GET | `/calculations/{id}` | Read a specific calculation |
| POST | `/calculations` | Add a new calculation |
| PUT | `/calculations/{id}` | Edit an existing calculation |
| DELETE | `/calculations/{id}` | Delete a calculation |

---

# Testing

The project includes:

- Unit tests
- Integration tests
- Playwright end-to-end tests

The tests verify:

- User registration
- User login
- JWT authentication
- Calculation BREAD operations
- Database persistence
- Input validation
- Division-by-zero handling
- User authorization and ownership protection

---

# Continuous Integration

GitHub Actions automatically:

- Installs project dependencies
- Starts PostgreSQL
- Runs unit and integration tests
- Runs Playwright end-to-end tests
- Builds the Docker image

---

# Docker Hub

Docker image:

https://hub.docker.com/r/swathi638/fastapi-calculator

---

# Reflection

This project expanded a simple calculator into a secure full-stack web application by implementing JWT authentication, PostgreSQL persistence, and complete BREAD functionality for user calculations. Integration tests and Playwright end-to-end tests helped verify both backend APIs and user interactions, while Docker and GitHub Actions provided a consistent development and deployment workflow. Troubleshooting issues involving authentication, database connectivity, and Playwright browser configuration strengthened my understanding of full-stack development, automated testing, containerization, and continuous integration.

---

# Author

**Swathi Veerapalli**