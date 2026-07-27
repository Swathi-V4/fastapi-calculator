import time

from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:8000"


def test_successful_registration(page: Page):
    unique_id = int(time.time())
    username = f"playwright{unique_id}"
    email = f"playwright{unique_id}@example.com"

    page.goto(f"{BASE_URL}/register-page")

    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", "Password123")
    page.fill("#confirm-password", "Password123")
    page.click("button[type='submit']")

    expect(page.locator("#message")).to_have_text(
        "Registration successful!"
    )


def test_successful_login(page: Page):
    unique_id = int(time.time())
    username = f"loginuser{unique_id}"
    email = f"loginuser{unique_id}@example.com"
    password = "Password123"

    page.goto(f"{BASE_URL}/register-page")
    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", password)
    page.fill("#confirm-password", password)
    page.click("button[type='submit']")

    expect(page.locator("#message")).to_have_text(
        "Registration successful!"
    )

    page.goto(f"{BASE_URL}/login-page")
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("button[type='submit']")

    expect(page.locator("#message")).to_have_text(
        "Login successful!"
    )

    token = page.evaluate(
        "() => localStorage.getItem('access_token')"
    )
    assert token is not None
    assert len(token) > 20


def test_registration_with_short_password(page: Page):
    page.goto(f"{BASE_URL}/register-page")

    page.fill("#username", "shortpassworduser")
    page.fill("#email", "shortpassword@example.com")
    page.fill("#password", "short")
    page.fill("#confirm-password", "short")

    page.evaluate(
        """
        document.querySelector("#password").removeAttribute("minlength");
        document.querySelector("#confirm-password").removeAttribute("minlength");
        """
    )

    page.click("button[type='submit']")

    expect(page.locator("#message")).to_have_text(
        "Password must be at least 8 characters."
    )


def test_login_with_wrong_password(page: Page):
    unique_id = int(time.time())
    username = f"wrongpass{unique_id}"
    email = f"wrongpass{unique_id}@example.com"

    page.goto(f"{BASE_URL}/register-page")
    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", "Password123")
    page.fill("#confirm-password", "Password123")
    page.click("button[type='submit']")

    expect(page.locator("#message")).to_have_text(
        "Registration successful!"
    )

    page.goto(f"{BASE_URL}/login-page")
    page.fill("#email", email)
    page.fill("#password", "WrongPassword123")
    page.click("button[type='submit']")

    expect(page.locator("#message")).to_have_text(
        "Invalid email or password"
    )