import pytest
from playwright.sync_api import expect


@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    page.goto("http://localhost:8000")

    expect(page.locator("h1")).to_have_text("Hello World")


@pytest.mark.e2e
def test_calculator_add(page, fastapi_server):
    page.goto("http://localhost:8000")

    page.fill("#a", "10")
    page.fill("#b", "5")
    page.click('button:text("Add")')

    # Playwright waits until the asynchronous request finishes.
    expect(page.locator("#result")).to_have_text(
        "Calculation Result: 15"
    )


@pytest.mark.e2e
def test_calculator_divide_by_zero(page, fastapi_server):
    page.goto("http://localhost:8000")

    page.fill("#a", "10")
    page.fill("#b", "0")
    page.click('button:text("Divide")')

    # Playwright waits until the error response appears.
    expect(page.locator("#result")).to_have_text(
        "Error: Cannot divide by zero!"
    )