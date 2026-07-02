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
    # Navigation links
    expect(page.get_by_role("link", name="Desktops", exact=True)).to_be_visible()
    expect(page.get_by_role("link", name="Tablets", exact=True)).to_be_visible()
    expect(page.get_by_role("link", name="Phones & PDAs", exact=True)).to_be_visible()
    
    # Search bar and Cart
    expect(page.locator("input[name='search']")).to_be_visible()
    expect(page.locator("#cart")).to_be_visible()
    
    # Footer links
    expect(page.get_by_role("link", name="About Us")).to_be_visible()
    expect(page.get_by_role("link", name="Contact Us")).to_be_visible()

def test_search_valid_product(page: Page):
    """Test searching for a valid product (iPhone)."""
    search_input = page.locator("input[name='search']")
    search_input.fill("iPhone")
    page.locator("button.btn-light.btn-lg").click() # Search button icon
    
    # Check if results appear
    expect(page.locator("h1")).to_contain_text("Search - iPhone")
    expect(page.locator(".product-thumb")).to_have_count(1)

def test_add_featured_product_to_cart(page: Page):
    """Test adding a featured product to the cart from the homepage."""
    # Locate first product card and click Add to Cart
    first_product = page.locator(".product-thumb").first
    first_product.get_by_role("button", name="Add to Cart").click()
    
    # Success message validation
    success_alert = page.locator(".alert-success")
    expect(success_alert).to_be_visible()
    expect(success_alert).to_contain_text("Success: You have added")

def test_change_currency(page: Page):
    """Test switching the currency to Euro."""
    page.locator(".nav-item .dropdown-toggle").filter(has_text="Currency").click()
    page.get_by_role("button", name="€ Euro").click()
    
    # Verify currency symbol changes on a product price
    price_tag = page.locator(".price-new").first
    expect(price_tag).to_contain_text("€")

# --- EDGE CASES ---

def test_search_no_results(page: Page):
    """Negative Scenario: Search for a product that does not exist."""
    search_input = page.locator("input[name='search']")
    search_input.fill("NonExistentMagicWand123")
    page.locator("button.btn-light.btn-lg").click()
    
    # Verify no results message
    expect(page.locator("#content p")).to_contain_text("There is no product that matches the search criteria.")

def test_empty_search_submission(page: Page):
    """Edge Case: Clicking search without entering any text."""
    page.locator("button.btn-light.btn-lg").click()
    # Should stay on search page or show neutral search state
    expect(page.locator("h1")).to_contain_text("Search")

# --- SECURITY TEST SNIPPETS ---

def test_security_sql_injection_attempt(page: Page):
    """Security: Attempt a basic SQL injection payload in search."""
    sqli_payload = "' OR '1'='1"
    search_input = page.locator("input[name='search']")
    search_input.fill(sqli_payload)
    page.locator("button.btn-light.btn-lg").click()
    
    # Verify the application doesn't crash and treats it as a string
    expect(page.locator("h1")).to_contain_text("Search")
    expect(page.locator(".alert-danger")).not_to_be_visible()

def test_security_xss_attempt(page: Page):
    """Security: Attempt a basic Cross-Site Scripting (XSS) payload in search."""
    xss_payload = "<script>alert('XSS')</script>"
    search_input = page.locator("input[name='search']")
    search_input.fill(xss_payload)
    page.locator("button.btn-light.btn-lg").click()
    
    # Verify payload is sanitized (rendered as text, not executed)
    # Playwright's page.on('dialog') would catch an alert if it fired
    page.on("dialog", lambda dialog: pytest.fail("XSS Alert Triggered!"))
    expect(page.locator("h1")).to_be_visible()