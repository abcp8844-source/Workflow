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
        context = browser.new_context(
            storage_state=STATE_PATH, 
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        )
        page = context.new_page()
        
        # براہ راست گروپ کا پوسٹ باکس لنک (یہ سب سے بڑا شارٹ کٹ ہے)
        post_url = f"https://m.facebook.com/groups/{GROUP_ID}/composer/"
        page.goto(post_url, wait_until="load")
        time.sleep(10)
        
        # اب کوئی بٹن نہیں ڈھونڈنا، سیدھا ٹیکسٹ ایریا پر فوکس کرنا ہے
        # موبائل براؤزر میں پہلا textarea ہی پوسٹ باکس ہوتا ہے
        page.keyboard.insert_text(message)
        time.sleep(5)
        
        # 'Post' بٹن کو رول کے ذریعے کلک کریں، یہ کبھی نہیں بدلتا
        page.get_by_role("button", name="Post").click()
        time.sleep(15)
        
        # فائل اپ ڈیٹ
        posts.pop(0)
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        
        browser.close()

if __name__ == "__main__":
    post_to_facebook_group()
