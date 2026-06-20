import os
import json
import time
from playwright.sync_api import sync_playwright

GROUP_ID = "1403757117731031"
FILE_PATH = "pending_posts.json"
STATE_PATH = "auth_state.json"

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
        # موبائل موڈ لازمی ہے، ورنہ فیس بک نہیں چلے گا
        context = browser.new_context(
            storage_state=STATE_PATH,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )
        page = context.new_page()
        
        # ڈائریکٹ گروپ پوسٹ کمپوزر لنک
        url = f"https://m.facebook.com/groups/{GROUP_ID}/"
        page.goto(url, wait_until="networkidle")
        time.sleep(10)
        
        # اس بار ہم کلک نہیں کریں گے، سیدھا باکس کو تلاش کر کے بھریں گے
        # موبائل فیس بک کا ٹیکسٹ باکس ہمیشہ یہی رہتا ہے
        try:
            # سیدھا ٹیکسٹ ایریا میں لکھیں
            page.fill("textarea", message)
            time.sleep(5)
            # پوسٹ بٹن
            page.click("input[type='submit']")
            time.sleep(15)
            
            posts.pop(0)
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            # ڈیبگنگ کے لیے سکرین شاٹ
            page.screenshot(path="final_debug.png")
            raise e
        
        browser.close()

if __name__ == "__main__":
    post_to_facebook_group()
