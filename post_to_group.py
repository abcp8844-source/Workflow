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
    message = f"{current_post['title']}\n\nExcellence meets opportunity. At our platform, we believe that your career deserves nothing less than verified precision. We filter out the noise and the scams to bring you only the most authentic, globally verified opportunities.\n\n👉 Apply Here: {current_post['link']}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=STATE_PATH, 
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        )
        page = context.new_page()
        
        # ٹائم آؤٹ بڑھا دیا ہے اور نیویگیشن کا طریقہ تبدیل کر دیا ہے
        try:
            page.goto(f"https://m.facebook.com/groups/{GROUP_ID}/", timeout=60000, wait_until="commit")
            time.sleep(15) # پیج لوڈ ہونے کے لیے مزید وقت
            page.screenshot(path="debug_start.png")
            
            # پوسٹ باکس تلاش کریں (موبائل ورژن میں 'Write something' کے لیے یہ سب سے بیسٹ ہے)
            page.locator("div[class*='_55wr']").first.click()
            time.sleep(5)
            
            page.keyboard.insert_text(message)
            time.sleep(5)
            
            # 'Post' بٹن پر کلک
            page.locator("button[value='Post']").click()
            time.sleep(15)
            
            # کامیابی پر لسٹ اپ ڈیٹ
            posts.pop(0)
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            page.screenshot(path="error_final.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    post_to_facebook_group()
