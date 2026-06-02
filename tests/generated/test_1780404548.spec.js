import pytest
from playwright.sync_api import Page, expect

# Base URL of the local development environment
BASE_URL = 'http://localhost:5173'

def test_page_loads_successfully(page: Page):
    """
    Happy Path: Verifies that the page loads successfully,
    the page title is visible, and the main heading is present.
    """
    # Navigate to localhost
    page.goto(BASE_URL)

    # Verify the page title metadata is not empty
    title = page.title()
    assert len(title) > 0, 'Page title metadata should not be empty'

    # Expect the main page heading (H1) to be visible
    main_heading = page.locator('h1').first
    expect(main_heading).to_be_visible(timeout=5000)

def test_main_navigation_links(page: Page):
    """
    Happy Path: Verifies that navigation links are present and functional.
    """
    page.goto(BASE_URL)

    # Target generic navigation link elements
    nav_links = page.locator('nav a, header a, [role="navigation"] a')

    # Skip test if the app does not feature navigation links yet
    if nav_links.count() == 0:
        pytest.skip('No navigation links found to test.')

    # Assert navigation links are visible and enabled
    first_link = nav_links.first
    expect(first_link).to_be_visible()
    expect(first_link).to_be_enabled()

    # Click the first navigation link and assert it does not crash
    first_link.click()
    page.wait_for_load_state('domcontentloaded')
    expect(page.locator('body')).to_be_visible()

def test_primary_action_button(page: Page):
    """
    Happy Path: Checks that the primary action button is visible, enabled, and clickable.
    """
    page.goto(BASE_URL)

    # Try to locate a primary CTA button using common class names, roles, or text
    primary_btn = page.locator("button[type='submit'], button.btn-primary, button:has-text('Get Started'), button:has-text('Submit'), [role='button']").first

    # Fallback to any button if specific patterns aren't matched
    if primary_btn.count() == 0:
        primary_btn = page.locator('button').first

    # Skip test if there are no buttons on the page
    if primary_btn.count() == 0:
        pytest.skip('No action buttons found to test.')

    # Assert button is interactive
    expect(primary_btn).to_be_visible()
    expect(primary_btn).to_be_enabled()
    
    # Trigger click action
    primary_btn.click()

def test_responsive_mobile_viewport(page: Page):
    """
    Edge Case: Tests layout responsiveness and navigation visibility on a mobile viewport.
    """
    # Set viewport to mobile dimension
    page.set_viewport_size({'width': 375, 'height': 812})
    page.goto(BASE_URL)

    # Find hamburger menu button if present
    mobile_menu_button = page.locator("button[aria-label*='menu'], button[class*='menu'], .hamburger").first

    if mobile_menu_button.is_visible():
        # Open navigation using the toggle button
        mobile_menu_button.click()
        nav_links = page.locator('nav a, header a, [role="navigation"] a')
        expect(nav_links.first).to_be_visible()
    else:
        # If no custom mobile menu button, verify main content still fits cleanly
        main_heading = page.locator('h1').first
        expect(main_heading).to_be_visible()

def test_no_critical_console_errors_on_load(page: Page):
    """
    Negative Scenario: Ensures the application loads cleanly with no severe console errors or uncaught exceptions.
    """
    console_errors = []

    # Intercept console messages and save error logs
    page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)

    page.goto(BASE_URL)
    page.wait_for_load_state('networkidle')

    # Filter errors to find critical app failures, ignoring common dev tool warnings
    critical_errors = [err for err in console_errors if 'failed to load' in err.lower() or 'exception' in err.lower()]

    assert len(critical_errors) == 0, f'Uncaught console errors detected on page load: {critical_errors}'
