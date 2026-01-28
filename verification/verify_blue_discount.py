
import os
import json
from playwright.sync_api import sync_playwright, expect

def verify_blue_discount(page):
    print("Navigating to app...")
    page.goto("http://localhost:5002")
    
    # Mock User
    user = {
        "id": "test-user-1",
        "name": "Test Student",
        "role": "STUDENT",
        "credits": 100,
        "isPremium": False
    }
    
    # Mock Settings
    settings = {
        "specialDiscountEvent": {
            "enabled": True,
            "eventName": "Blue Sale",
            "discountPercent": 50,
            "startsAt": "2024-01-01T00:00:00.000Z",
            "endsAt": "2099-01-01T00:00:00.000Z"
        }
    }
    
    print("Injecting state...")
    page.evaluate(f"localStorage.setItem('nst_current_user', '{json.dumps(user)}');")
    page.evaluate("localStorage.setItem('nst_users', JSON.stringify([JSON.parse(localStorage.getItem('nst_current_user'))]));")
    page.evaluate(f"localStorage.setItem('nst_system_settings', '{json.dumps(settings)}');")

    print("Reloading...")
    page.reload()
    
    # Wait for Dashboard
    try:
        page.wait_for_selector("text=Test Student", timeout=10000)
    except:
        print("Dashboard load failed.")
        return

    # Verify Discount Banner styling via screenshot or class inspection if possible
    # We will look for "Blue Sale" text
    try:
        expect(page.get_by_text("Blue Sale")).to_be_visible()
        print("PASS: Banner Title correct.")
    except Exception as e:
        print(f"FAIL: Banner not found: {e}")

    # Take screenshot to verify Blue Theme
    page.screenshot(path="verification/blue_discount_check.png")
    print("Screenshot saved to verification/blue_discount_check.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_blue_discount(page)
        finally:
            browser.close()
