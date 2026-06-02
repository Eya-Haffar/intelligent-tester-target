import pytest
from playwright.sync_api import Page, expect

BASE_URL = 'http://localhost:5173'

def test_todo_app_title(page: Page):
    """Test that the application loads and has the correct title."""
    page.goto(BASE_URL)
    expect(page).to_have_title("Todo App")

def test_add_todo_item(page: Page):
    """Test adding a new todo item."""
    page.goto(BASE_URL)
    
    # Locate the input field and the add button
    input_field = page.get_by_placeholder("Enter todo...")
    add_button = page.locator("button", has_text="Add")
    
    # Type a new todo and click add
    input_field.fill("Buy groceries")
    add_button.click()
    
    # Verify the todo was added to the list
    todo_item = page.locator("li", has_text="Buy groceries")
    expect(todo_item).to_be_visible()

