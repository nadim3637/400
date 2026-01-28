import json
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()

    # Mock Admin User
    user = {
        "id": "admin-1",
        "name": "Test User",
        "role": "ADMIN",
        "isPremium": True
    }

    try:
        # Navigate to app
        page.goto("http://localhost:5000")
        
        # Inject user into localStorage
        page.evaluate(f"localStorage.setItem('nst_current_user', '{json.dumps(user)}')")
        
        # Reload to pick up user
        page.reload()
        page.wait_for_timeout(5000)
        
        # 1. Verify Dashboard Tiles
        page.screenshot(path="verification/dashboard_view.png")
        print("Dashboard screenshot taken.")
        
        # Check for "Marksheet" tile
        marksheet_btn = page.get_by_text("Marksheet", exact=True)
        if marksheet_btn.is_visible():
            print("Marksheet button found.")
            marksheet_btn.click()
            page.wait_for_timeout(3000)
            page.screenshot(path="verification/marksheet_modal.png")
            print("Marksheet modal screenshot taken.")
        else:
            print("Marksheet button NOT found.")

    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="verification/error.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
