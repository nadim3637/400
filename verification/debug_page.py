from playwright.sync_api import sync_playwright

def debug(page):
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
    
    page.screenshot(path="verification/debug_state.png")
    print("Screenshot saved to verification/debug_state.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            debug(page)
        finally:
            browser.close()
