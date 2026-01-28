from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to home
        try:
            print("Navigating to http://localhost:5001...")
            page.goto("http://localhost:5001", timeout=60000)
            
            # Wait a bit for React to hydrate
            time.sleep(5)
            
            # Take screenshot
            page.screenshot(path="verification/dashboard_view.png", full_page=True)
            print("Screenshot taken: dashboard_view.png")
            
            # Check for Performance Trend text
            # It might be visible if we are logged in by default (dev mode often mocks user)
            # If not, we might be on login page.
            if page.get_by_text("Performance Trend").is_visible():
                print("Performance Trend is visible.")
            else:
                print("Performance Trend NOT visible.")
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
