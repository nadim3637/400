
import json
import time
from playwright.sync_api import sync_playwright, expect

def verify_discount_logic(page):
    print("Setting up user...")
    user_data = {
        "id": "test-user-discount",
        "name": "Discount User",
        "role": "STUDENT",
        "classLevel": "10",
        "board": "CBSE",
        "stream": "Science",
        "isPremium": False,
        "credits": 100
    }
    page.goto("http://localhost:5173")
    page.evaluate(f"localStorage.setItem('nst_current_user', '{json.dumps(user_data)}');")
    page.evaluate("localStorage.setItem('nst_has_seen_welcome', 'true');") # Skip welcome
    
    # 1. TEST: DISABLED
    print("\n--- TEST 1: Discount DISABLED ---")
    settings_disabled = {
        "specialDiscountEvent": {
            "enabled": False,
            "eventName": "Test Sale",
            "discountPercent": 50,
            "startsAt": (time.time() * 1000) + 3600000, # Future
            "endsAt": (time.time() * 1000) + 7200000
        }
    }
    page.evaluate(f"localStorage.setItem('nst_system_settings', '{json.dumps(settings_disabled)}');")
    page.reload()
    expect(page.get_by_text("Discount User")).to_be_visible() # Wait for dashboard
    
    # Check Banner
    banner = page.get_by_text("Test Sale")
    if banner.count() > 0 and banner.is_visible():
        print("FAILED: Banner visible when disabled!")
        exit(1)
    else:
        print("PASSED: Banner hidden.")

    # 2. TEST: WAITING (STARTS SOON)
    print("\n--- TEST 2: WAITING (Future Start) ---")
    now_ms = time.time() * 1000
    settings_waiting = {
        "specialDiscountEvent": {
            "enabled": True,
            "eventName": "Future Sale",
            "discountPercent": 50,
            "startsAt": now_ms + 3600000, # +1 Hour
            "endsAt": now_ms + 7200000
        }
    }
    page.evaluate(f"localStorage.setItem('nst_system_settings', '{json.dumps(settings_waiting)}');")
    page.reload()
    expect(page.get_by_text("Discount User")).to_be_visible()
    
    # Expect "Future Sale" and "STARTS IN"
    expect(page.get_by_text("Future Sale")).to_be_visible()
    expect(page.get_by_text("STARTS IN")).to_be_visible()
    print("PASSED: Banner shows 'STARTS IN'.")
    
    # 3. TEST: ACTIVE
    print("\n--- TEST 3: ACTIVE (Past Start) ---")
    settings_active = {
        "specialDiscountEvent": {
            "enabled": True,
            "eventName": "Active Sale",
            "discountPercent": 50,
            "startsAt": now_ms - 3600000, # -1 Hour
            "endsAt": now_ms + 3600000    # +1 Hour
        }
    }
    page.evaluate(f"localStorage.setItem('nst_system_settings', '{json.dumps(settings_active)}');")
    page.reload()
    expect(page.get_by_text("Discount User")).to_be_visible()
    
    # Expect "Active Sale" and "ENDS IN"
    expect(page.get_by_text("Active Sale")).to_be_visible()
    expect(page.get_by_text("ENDS IN")).to_be_visible()
    print("PASSED: Banner shows 'ENDS IN'.")

    print("\nAll Discount Logic Verified Successfully!")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_discount_logic(page)
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="/home/jules/verification/discount_error.png")
            raise e
        finally:
            browser.close()
