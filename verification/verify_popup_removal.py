
import os
import json
import time
from playwright.sync_api import sync_playwright, expect

def test_popup_removal_and_analytics_review(page):
    print("Setting up user in localStorage...")
    
    # Mock User Data
    user_data = {
        "id": "test-user-123",
        "name": "Test Student",
        "role": "STUDENT",
        "classLevel": "10",
        "board": "CBSE",
        "stream": "Science",
        "isPremium": False,
        "credits": 100,
        "createdAt": "2023-01-01T00:00:00.000Z",
        # Add some history for analytics
        "mcqHistory": [
            {
                "id": "test-1",
                "date": "2023-01-01T00:00:00.000Z",
                "score": 8,
                "totalQuestions": 10,
                "correctCount": 8,
                "wrongCount": 2,
                "totalTimeSeconds": 120,
                "averageTimePerQuestion": 12,
                "performanceTag": "GOOD",
                "chapterTitle": "Chemical Reactions",
                "subjectName": "Science",
                "classLevel": "10"
            }
        ]
    }
    
    # Inject localStorage
    page.goto("http://localhost:5173")
    page.evaluate(f"localStorage.setItem('nst_current_user', '{json.dumps(user_data)}');")
    page.evaluate("localStorage.setItem('nst_has_seen_welcome', 'false');") # Force welcome condition if logic existed
    
    print("Reloading to apply user...")
    page.reload()
    
    print("Waiting for Dashboard...")
    # Wait for a dashboard element
    expect(page.get_by_text("Test Student")).to_be_visible(timeout=10000)
    
    # 1. VERIFY POPUP REMOVAL
    print("Verifying Popup Removal...")
    # Wait a bit to ensure no popup appears (since it had a timeout/interval)
    time.sleep(3) 
    
    # Check for text specific to ThreeTierPopup
    # "Free Plan", "Basic Plan", "Ultra Plan"
    # "GET ULTRA NOW"
    
    popup_texts = ["Free Plan", "Basic Plan", "Ultra Plan", "GET ULTRA NOW"]
    for text in popup_texts:
        count = page.get_by_text(text).count()
        if count > 0:
             # It might be in the DOM but hidden? Or confusing with Store?
             # ThreeTierPopup is fixed inset-0 z-[200].
             # We should check if visible.
             if page.get_by_text(text).first.is_visible():
                 print(f"FAILED: Popup text '{text}' is visible!")
                 page.screenshot(path="/home/jules/verification/failed_popup.png")
                 exit(1)
             else:
                 print(f"Text '{text}' found but not visible (might be elsewhere). Good.")
        else:
             print(f"Text '{text}' not found. Good.")

    print("Popup check passed. Taking Dashboard screenshot...")
    page.screenshot(path="/home/jules/verification/dashboard_clean.png")
    
    # 2. VERIFY ANALYTICS PAGE (No Review Button)
    print("Navigating to Analytics...")
    # Click on "Analytics" in Quick Actions or Profile
    # Assuming "Analytics" button exists in "Quick Actions" grid
    page.get_by_text("Analytics", exact=True).click()
    
    # Wait for Analytics Page
    expect(page.get_by_text("Annual Report")).to_be_visible()
    
    print("Checking Recent Tests for Review Button...")
    # Find "Recent Tests" section
    recent_tests = page.get_by_text("Recent Tests")
    expect(recent_tests).to_be_visible()
    
    # In Recent Tests, we should see "Chemical Reactions" (from mock history)
    expect(page.get_by_text("Chemical Reactions")).to_be_visible()
    
    # Check for "Review" button
    # We expect "Marksheet" button to be there
    expect(page.get_by_role("button", name="Marksheet")).to_be_visible()
    
    # "Review" button should NOT be there
    review_btn = page.get_by_role("button", name="Review")
    if review_btn.count() > 0 and review_btn.is_visible():
        print("FAILED: 'Review' button is visible in Recent Tests!")
        page.screenshot(path="/home/jules/verification/failed_analytics.png")
        exit(1)
    else:
        print("'Review' button NOT found. Good.")
        
    print("Taking Analytics screenshot...")
    page.screenshot(path="/home/jules/verification/analytics_clean.png")
    
    print("Verification Successful!")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_popup_removal_and_analytics_review(page)
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="/home/jules/verification/error.png")
            raise e
        finally:
            browser.close()
