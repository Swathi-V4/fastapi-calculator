# Running Tests Locally

Clone the repository:

```bash
git clone https://github.com/Swathi-V4/fastapi-calculator.git
cd fastapi-calculator
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
pytest -v
```

Run only unit tests:

```bash
pytest tests/unit -v
```

Run only integration tests:

```bash
pytest tests/integration -v
```

Run only end-to-end tests:

```bash
pytest tests/e2e -v
```

# Docker Hub Repository

Docker image:

https://hub.docker.com/r/swathi638/fastapi-calculator