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

    # 1. Dismiss Daily Goal Tracker Popup
    # Try finding "Continue Learning" button
    try:
        page.get_by_text("Continue Learning").click(timeout=5000)
        print("Dismissed Daily Goal Tracker")
        page.wait_for_timeout(1000)
    except:
        print("Tracker popup not found or already closed")

    # 2. Click Admin Panel
    # Use the button in the fixed container
    # It might be an icon button, so text might be hidden or small.
    # Looking at code: <span className="font-bold text-xs">Admin Panel</span>
    page.get_by_text("Admin Panel").click()
    page.wait_for_timeout(2000)

    # 3. In Admin Dashboard -> Challenge 2.0
    page.get_by_text("Challenge 2.0").click()
    page.wait_for_timeout(1000)

    # 4. Select Import Mode (Paste button)
    # The button text is "Paste" inside a span
    page.get_by_text("Paste").click()
    
    # 5. Paste Data
    data = "Q1\tA\tB\tC\tD\t1\tExp1\nQ2\tX\tY\tZ\tW\t2\tExp2"
    page.get_by_placeholder("Question 1").fill(data)
    
    # 6. Process
    page.get_by_text("Process & Preview").click()
    page.wait_for_timeout(1000)

    # 7. Verify Questions appear
    expect(page.get_by_text("Q1. Q1")).to_be_visible()
    expect(page.get_by_text("Q2. Q2")).to_be_visible()

    # Take Screenshot
    page.screenshot(path="verification/import_success.png")
    print("Success! Screenshot saved.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            test_import_and_challenge(page)
        except Exception as e:
            print(f"Verification Failed: {e}")
            page.screenshot(path="verification/error_resolved.png")
        finally:
            browser.close()
