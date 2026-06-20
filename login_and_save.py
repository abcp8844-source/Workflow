import os
import time
from playwright.sync_api import sync_playwright

FB_EMAIL = os.environ.get("FB_EMAIL")
FB_PASSWORD = os.environ.get("FB_PASSWORD")
STATE_PATH = "auth_state.json"

def run_initial_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("Navigating to Facebook...")
        page.goto("https://www.facebook.com/login")
        time.sleep(5)
        
        print("Entering credentials...")
        page.fill("input[name='email']", FB_EMAIL)
        time.sleep(1.5)
        page.fill("input[name='pass']", FB_PASSWORD)
        time.sleep(1.5)
        
        print("Locating login button...")
        login_selectors = [
            "button[name='login']",
            "button[type='submit']",
            "[data-testid='royal_login_button']",
            "text=Log In"
        ]
        
        clicked = False
        for selector in login_selectors:
            if page.locator(selector).is_visible():
                page.click(selector)
                clicked = True
                print(f"Clicked login button using selector: {selector}")
                break
                
        if not clicked:
            print("Standard selectors not visible, trying fallback click...")
            page.click("button")
        
        print("Waiting for login to complete. Checking for redirect...")
        page.wait_for_url("https://www.facebook.com/**", timeout=60000)
        
        time.sleep(5)
        
        context.storage_state(path=STATE_PATH)
        print(f"Login successful! Session state saved to {STATE_PATH}")
        
        browser.close()

if __name__ == "__main__":
    run_initial_login()
