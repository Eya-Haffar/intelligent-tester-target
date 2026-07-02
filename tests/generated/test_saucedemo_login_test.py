import pytest
from playwright.sync_api import Page, expect

# ── SauceDemo Login Flow Tests ──
# Generated for: https://www.saucedemo.com

BASE_URL = "https://www.saucedemo.com"

def test_valid_login_redirects_to_products(page: Page):
    """Valid login should redirect to the inventory/products page."""
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")
    expect(page.locator(".inventory_list")).to_be_visible()

def test_invalid_login_shows_error(page: Page):
    """Invalid credentials should display an error message."""
    page.goto(BASE_URL)
    page.fill("#user-name", "wrong_user")
    page.fill("#password", "wrong_pass")
    page.click("#login-button")
    error = page.locator("[data-test=error]")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")

def test_empty_username_shows_error(page: Page):
    """Empty username should show validation error."""
    page.goto(BASE_URL)
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    error = page.locator("[data-test=error]")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username is required")

def test_locked_user_cannot_login(page: Page):
    """Locked out user should see specific error message."""
    page.goto(BASE_URL)
    page.fill("#user-name", "locked_out_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    error = page.locator("[data-test=error]")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Sorry, this user has been locked out")
