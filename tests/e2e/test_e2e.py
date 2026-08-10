import os
from uuid import uuid4

import pytest
from playwright.sync_api import expect


BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:8000",
)

PASSWORD = "Password123!"


@pytest.mark.e2e
def test_register_login_and_bread(page, fastapi_server):
    unique_value = uuid4().hex[:8]
    username = f"playwright_{unique_value}"
    email = f"playwright_{unique_value}@test.com"

    # Register
    page.goto(f"{BASE_URL}/register-page")

    page.locator("#username").fill(username)
    page.locator("#email").fill(email)
    page.locator("#password").fill(PASSWORD)
    page.locator("#confirm-password").fill(PASSWORD)

    page.get_by_role("button", name="Register").click()

    expect(page.locator("#message")).to_contain_text(
        "Registration successful"
    )

    # Login
    page.goto(f"{BASE_URL}/login-page")

    page.locator("#email").fill(email)
    page.locator("#password").fill(PASSWORD)

    page.get_by_role("button", name="Login").click()

    expect(page.locator("#message")).to_contain_text(
        "Login successful"
    )

    page.wait_for_url(f"{BASE_URL}/")

    # Add
    page.locator("#a").fill("10")
    page.locator("#b").fill("5")
    page.locator("#type").select_option("Add")

    page.locator("#submit-button").click()

    expect(page.locator("#message")).to_contain_text(
        "Calculation added successfully"
    )

    calculation_row = page.locator(
        "#calculation-table-body tr"
    ).first

    expect(calculation_row).to_contain_text("10")
    expect(calculation_row).to_contain_text("5")
    expect(calculation_row).to_contain_text("Add")
    expect(calculation_row).to_contain_text("15")

    # Read
    calculation_row.get_by_role(
        "button",
        name="View",
        exact=True,
    ).click()

    expect(page.locator("#details")).to_be_visible()
    expect(page.locator("#details-content")).to_contain_text(
        "Result:"
    )
    expect(page.locator("#details-content")).to_contain_text(
        "15"
    )

    # Edit
    calculation_row.get_by_role(
        "button",
        name="Edit",
        exact=True,
    ).click()

    expect(page.locator("#form-title")).to_contain_text(
        "Edit Calculation"
    )

    page.locator("#a").fill("20")
    page.locator("#b").fill("2")
    page.locator("#type").select_option("Multiply")

    page.locator("#submit-button").click()

    expect(page.locator("#message")).to_contain_text(
        "Calculation updated successfully"
    )

    calculation_row = page.locator(
        "#calculation-table-body tr"
    ).first

    expect(calculation_row).to_contain_text("20")
    expect(calculation_row).to_contain_text("2")
    expect(calculation_row).to_contain_text("Multiply")
    expect(calculation_row).to_contain_text("40")

    # Delete
    page.once("dialog", lambda dialog: dialog.accept())

    calculation_row.get_by_role(
        "button",
        name="Delete",
        exact=True,
    ).click()

    expect(page.locator("#message")).to_contain_text(
        "Calculation deleted successfully"
    )

    expect(
        page.locator("#calculation-table-body tr")
    ).to_have_count(0)

    expect(page.locator("#empty-state")).to_be_visible()


@pytest.mark.e2e
def test_power_calculation(page, fastapi_server):
    """
    Verify the new Power feature through the browser.
    """
    unique_value = uuid4().hex[:8]
    username = f"poweruser_{unique_value}"
    email = f"poweruser_{unique_value}@test.com"

    # Register
    page.goto(f"{BASE_URL}/register-page")

    page.locator("#username").fill(username)
    page.locator("#email").fill(email)
    page.locator("#password").fill(PASSWORD)
    page.locator("#confirm-password").fill(PASSWORD)

    page.get_by_role("button", name="Register").click()

    expect(page.locator("#message")).to_contain_text(
        "Registration successful"
    )

    # Login
    page.goto(f"{BASE_URL}/login-page")

    page.locator("#email").fill(email)
    page.locator("#password").fill(PASSWORD)

    page.get_by_role("button", name="Login").click()

    expect(page.locator("#message")).to_contain_text(
        "Login successful"
    )

    page.wait_for_url(f"{BASE_URL}/")

    # Power: 2 ^ 5 = 32
    page.locator("#a").fill("2")
    page.locator("#b").fill("5")
    page.locator("#type").select_option("Power")

    page.locator("#submit-button").click()

    expect(page.locator("#message")).to_contain_text(
        "Calculation added successfully"
    )

    calculation_row = page.locator(
        "#calculation-table-body tr"
    ).first

    expect(calculation_row).to_contain_text("Power")
    expect(calculation_row).to_contain_text("32")


@pytest.mark.e2e
def test_login_invalid_password(page, fastapi_server):
    page.goto(f"{BASE_URL}/login-page")

    page.locator("#email").fill("fake@test.com")
    page.locator("#password").fill("WrongPassword123")

    page.get_by_role("button", name="Login").click()

    expect(page.locator("#message")).to_contain_text(
        "Invalid email or password"
    )


@pytest.mark.e2e
def test_division_by_zero_validation(page, fastapi_server):
    page.goto(BASE_URL)

    page.locator("#a").fill("10")
    page.locator("#b").fill("0")
    page.locator("#type").select_option("Divide")

    page.locator("#submit-button").click()

    expect(page.locator("#message")).to_contain_text(
        "Division by zero"
    )