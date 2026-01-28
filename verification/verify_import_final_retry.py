import os
from playwright.sync_api import sync_playwright, expect

def test_import_and_challenge(page):
    page.goto("http://localhost:3000")
    page.wait_for_timeout(5000)
    
    # Inject Admin User
    page.evaluate("""
        localStorage.setItem('nst_current_user', JSON.stringify({
            id: 'ADMIN_TEST',
            name: 'Admin User',
            role: 'ADMIN',
            credits: 9999,
            isPremium: true
        }));
    """)
    page.reload()
    page.wait_for_timeout(5000)

    # Debug: Print page content if button not found
    # content = page.content()
    # print(content[:1000])

    # Try to find the button by the text span directly
    page.locator("span", has_text="Admin Panel").click()
    page.wait_for_timeout(2000)

    # In Admin Dashboard
    # Click "Challenge 2.0" card
    page.get_by_text("Challenge 2.0").click()
    page.wait_for_timeout(1000)

    # Select Import Mode (Paste button)
    page.get_by_text("Paste").click()
    
    # Paste Data into textarea
    # Placeholder is "Question 1..."
    data = "Q1\tA\tB\tC\tD\t1\tExp1\nQ2\tX\tY\tZ\tW\t2\tExp2"
    page.get_by_placeholder("Question 1").fill(data)
    
    # Process
    page.get_by_text("Process & Preview").click()
    page.wait_for_timeout(1000)

    # Verify Questions appear
    expect(page.get_by_text("Q1. Q1")).to_be_visible()
    expect(page.get_by_text("Q2. Q2")).to_be_visible()

    # Take Screenshot
    page.screenshot(path="verification/import_success.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            test_import_and_challenge(page)
            print("Verification Script Passed")
        except Exception as e:
            print(f"Verification Failed: {e}")
            page.screenshot(path="verification/error.png")
        finally:
            browser.close()
