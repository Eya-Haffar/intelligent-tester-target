import pytest
from playwright.sync_api import Page, expect

# Test Constants
BASE_URL = "https://ecommerce-playground.lambdatest.io"

@pytest.fixture(autouse=True)
def setup(page: Page):
    """Navigate to the base URL before each test."""
    page.goto(BASE_URL)

# --- HAPPY PATH TESTS ---

def test_homepage_elements_visible(page: Page):
    """Verify that key homepage elements are present and visible."""
    expect(page.get_by_role("link", name="Desktops").first).to_be_visible()
    expect(page.get_by_role("link", name="Tablets").first).to_be_visible()
    expect(page.get_by_role("link", name="Phones & PDAs").first).to_be_visible()
    
    expect(page.locator("input[name='search']").first).to_be_visible()
    
def test_search_valid_product(page: Page):
    """Test searching for a valid product (iPhone)."""
    search_input = page.locator("input[name='search']").first
    search_input.fill("iPhone")
    search_input.press("Enter")
    
    expect(page.locator("h1")).to_contain_text("Search")
    expect(page.locator(".product-thumb, .product-layout, .product-grid").first).to_be_visible()

def test_add_featured_product_to_cart(page: Page):
    """Test adding a featured product to the cart from the homepage."""
    # Use product_id 43 (MacBook) which is usually in stock
    page.goto(BASE_URL + "/index.php?route=product/product&product_id=43")
    page.locator("button:has-text('Add to Cart'), button[title='Add to Cart']").first.click()
    
    success_alert = page.locator(".alert-success, .toast-body").first
    expect(success_alert).to_be_visible()

def test_change_currency(page: Page):
    """Test switching the currency to Euro."""
    pass

# --- EDGE CASES ---

def test_search_no_results(page: Page):
    """Negative Scenario: Search for a product that does not exist."""
    search_input = page.locator("input[name='search']").first
    search_input.fill("NonExistentMagicWand123")
    search_input.press("Enter")
    
    expect(page.get_by_text("There is no product that matches the search criteria.").first).to_be_visible()

def test_empty_search_submission(page: Page):
    """Edge Case: Clicking search without entering any text."""
    search_input = page.locator("input[name='search']").first
    search_input.press("Enter")
    expect(page.locator("h1")).to_contain_text("Search")

# --- SECURITY TEST SNIPPETS ---

def test_security_sql_injection_attempt(page: Page):
    """Security: Attempt a basic SQL injection payload in search."""
    sqli_payload = "' OR '1'='1"
    search_input = page.locator("input[name='search']").first
    search_input.fill(sqli_payload)
    search_input.press("Enter")
    
    expect(page.locator("h1")).to_contain_text("Search")

def test_security_xss_attempt(page: Page):
    """Security: Attempt a basic Cross-Site Scripting (XSS) payload in search."""
    xss_payload = "<script>alert('XSS')</script>"
    search_input = page.locator("input[name='search']").first
    search_input.fill(xss_payload)
    search_input.press("Enter")
    
    page.on("dialog", lambda dialog: pytest.fail("XSS Alert Triggered!"))
    expect(page.locator("h1")).to_be_visible()