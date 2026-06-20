import os
import json
import time
from playwright.sync_api import sync_playwright

GROUP_ID = "1403757117731031"
STATE_PATH = "auth_state.json"
FILE_PATH = "pending_posts.json"

def post_to_facebook_group():
    if not os.path.exists(FILE_PATH): return
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try: posts = json.load(f)
        except: return
    if not posts: return

    current_post = posts[0]
    message = f"{current_post['title']}\n\n{current_post['link']}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # یہاں موبائل کا اصلی یوزر ایجنٹ سیٹ ہے
        context = browser.new_context(
            storage_state=STATE_PATH,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )
        page = context.new_page()
        
        # لاگ ان سٹیٹ چیک کریں
        page.goto("https://m.facebook.com/")
        time.sleep(5)
        
        # اگر لاگ ان نہیں ہے تو یہاں ایرر آئے گا
        if "login" in page.url:
            print("Cookies are expired or invalid!")
            return

        page.goto(f"https://m.facebook.com/groups/{GROUP_ID}/", wait_until="load")
        time.sleep(10)
        
        # اب ہم ایک ہڈن ان پٹ ڈھونڈتے ہیں جو ہمیشہ رہتا ہے
        page.fill("textarea[name='xc_message']", message)
        time.sleep(2)
        page.click("input[name='view_post']")
        time.sleep(10)
        
        posts.pop(0)
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        browser.close()

if __name__ == "__main__":
    post_to_facebook_group()
