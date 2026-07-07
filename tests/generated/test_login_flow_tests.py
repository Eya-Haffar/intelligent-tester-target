
from playwright.sync_api import Page, expect

def test_login_happy_path(page: Page):
    # Navigate to the login page
    page.goto('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
    # Fill in valid credentials
    page.fill('input[name="username"]', 'Admin')
    page.fill('input[name="password"]', 'admin123')
    # Submit the form
    page.click('button[type="submit"]')
    # Verify that we are redirected to the Dashboard page
    expect(page.locator('h6', has_text='Dashboard')).to_be_visible()

def test_login_invalid_credentials(page: Page):
    # Navigate to the login page
    page.goto('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
    # Fill in invalid credentials
    page.fill('input[name="username"]', 'Invalid')
    page.fill('input[name="password"]', 'invalid')
    # Submit the form
    page.click('button[type="submit"]')
    # Verify that the error message is displayed
    expect(page.locator('p', has_text='Invalid credentials')).to_be_visible()

def test_login_empty_fields(page: Page):
    # Navigate to the login page
    page.goto('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
    # Submit the form with empty fields
    page.click('button[type="submit"]')
    # Verify that the validation message is displayed for both fields
    expect(page.locator('span', has_text='Required')).to_have_count(2)

def test_login_empty_username(page: Page):
    # Navigate to the login page
    page.goto('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
    # Fill in a valid password
    page.fill('input[name="password"]', 'admin123')
    # Submit the form
    page.click('button[type="submit"]')
    # Verify that the validation message is displayed for the username field
    expect(page.locator('span', has_text='Required')).to_be_visible()

def test_login_empty_password(page: Page):
    # Navigate to the login page
    page.goto('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
    # Fill in a valid username
    page.fill('input[name="username"]', 'Admin')
    # Submit the form
    page.click('button[type="submit"]')
    # Verify that the validation message is displayed for the password field
    expect(page.locator('span', has_text='Required')).to_be_visible()
