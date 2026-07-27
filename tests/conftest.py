import time

import pytest
import requests


@pytest.fixture(scope="session")
def fastapi_server():
    """
    Confirm that the Docker-based FastAPI server is available
    before running the E2E tests.
    """
    server_url = "http://127.0.0.1:8000/"
    timeout = 30
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(
                server_url,
                timeout=2,
            )

            if response.status_code == 200:
                yield
                return

        except requests.RequestException:
            pass

        time.sleep(1)

    pytest.fail(
        "FastAPI server is not available at "
        "http://127.0.0.1:8000. "
        "Run 'docker compose up -d' first."
    )