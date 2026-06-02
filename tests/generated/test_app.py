import pytest
import re
from playwright.sync_api import Page, expect

# Base URL of your Vite React development server
BASE_URL = 'http://localhost:5173'

def test_homepage_loads_and_has_correct_title(page: Page):
    """Test that the application loads and displays the default Vite + React title."""
    page.goto(BASE_URL)
    
    # Expect the title to contain "Vite + React"
    expect(page).to_have_title(re.compile(r"Vite \+ React"))

def test_counter_increments_on_click(page: Page):
    """Test the interactivity of the default counter button."""
    page.goto(BASE_URL)
    
    # Locate the button that says "count is 0"
    counter_button = page.locator("button", has_text="count is 0")
    
    # Ensure it is visible on the page
    expect(counter_button).to_be_visible()
    
    # Click the button
    counter_button.click()
    
    # Verify that the text updates to "count is 1"
    updated_button = page.locator("button", has_text="count is 1")
    expect(updated_button).to_be_visible()
