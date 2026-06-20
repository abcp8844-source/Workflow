import os
import time
from playwright.sync_api import sync_playwright

FB_EMAIL = os.environ.get("FB_EMAIL")
FB_PASSWORD = os.environ.get("FB_PASSWORD")
STATE_PATH = "auth_state.json"

def run_initial_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # یوزر ایجنٹ کو اپ ڈیٹ رکھیں تاکہ فیس بک سکیورٹی الرٹ نہ دے
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("Navigating to Facebook...")
        page.goto("https://www.facebook.com/login")
        
        # انتظار کریں تاکہ پیج مکمل لوڈ ہو جائے
        page.wait_for_load_state("networkidle")
        
        print("Entering credentials...")
        page.fill("input[name='email']", FB_EMAIL)
        page.fill("input[name='pass']", FB_PASSWORD)
        
        print("Locating login button safely...")
        try:
            # یہ طریقہ "Strict Mode" والے ایرر کو نہیں آنے دے گا
            login_button = page.get_by_role("button", name="Log In").first
            login_button.click()
            print("Successfully clicked login button via Role selector.")
        except Exception as e:
            print(f"Role selector failed, trying fallback: {e}")
            # اگر پہلا طریقہ فیل ہو تو پرانے والے سلیکٹرز پر واپس جائیں
            page.locator("button[name='login']").click()
        
        print("Waiting for login to complete...")
        # فیس بک کے لاگ ان ہونے کا انتظار کریں
        page.wait_for_load_state("networkidle")
        time.sleep(10) # سیشن سیو کرنے سے پہلے تھوڑا وقت دیں
        
        # سیشن اسٹیٹ سیو کریں
        context.storage_state(path=STATE_PATH)
        print(f"Login successful! Session state saved to {STATE_PATH}")
        
        browser.close()

if __name__ == "__main__":
    run_initial_login()
