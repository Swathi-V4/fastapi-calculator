import os
import time

import pytest
import requests


BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:8000",
)


@pytest.fixture(scope="session")
def fastapi_server():
    """
    Confirm that the FastAPI server is available
    before running the E2E tests.
    """
    server_url = f"{BASE_URL}/"
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
        f"FastAPI server is not available at {BASE_URL}. "
        "Make sure the application is running first."
    )