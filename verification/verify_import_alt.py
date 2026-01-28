import os
from playwright.sync_api import sync_playwright, expect

def test_import_and_challenge(page):
    # 1. Login as Admin
    page.goto("http://localhost:3000")
    
    # Wait for app to load (basic check)
    page.wait_for_timeout(3000)
    
    # Inject Admin User
    page.evaluate("""
        localStorage.setItem('nst_current_user', JSON.stringify({
            id: 'ADMIN_TEST',
            name: 'Admin User',
            role: 'ADMIN',
            credits: 9999,
            isPremium: true
        }));
        
        // Also ensure settings exist
        if (!localStorage.getItem('nst_system_settings')) {
            localStorage.setItem('nst_system_settings', JSON.stringify({
                appName: 'Test App',
                specialDiscountEvent: { enabled: true, eventName: 'Test Event', endsAt: new Date(Date.now() + 86400000).toISOString() }
            }));
        }
    """)
    page.reload()
    page.wait_for_timeout(3000)

    # Click the "Admin Panel" button if found
    # Try multiple locators
    try:
        page.get_by_text("Admin Panel").click()
    except:
        print("Text locator failed, trying CSS selector")
        # Try to find the button with Layout icon or text
        page.locator("button:has-text('Admin Panel')").click()
        
    page.wait_for_timeout(2000)

    # Navigate to Challenge Creator 2.0
    # In Admin Dashboard, find the card "Challenge 2.0"
    page.get_by_text("Challenge 2.0").first.click()
    page.wait_for_timeout(1000)

    # Select Import Mode
    page.get_by_text("Paste").click()
    
    # Paste Data
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
