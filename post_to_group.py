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
        context = browser.new_context(storage_state=STATE_PATH, user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36")
        page = context.new_page()
        
        # 1. گروپ پیج
        page.goto(f"https://m.facebook.com/groups/{GROUP_ID}/")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="step1_page_load.png") # پہلا قدم
        time.sleep(5)

        try:
            # 2. باکس ڈھونڈنا
            page.get_by_placeholder("Write something...").click()
            page.screenshot(path="step2_box_clicked.png") # دوسرا قدم
            
            # 3. لکھنا
            page.keyboard.insert_text(message)
            time.sleep(2)
            
            # 4. پوسٹ بٹن
            page.get_by_role("button", name="Post").click()
            page.screenshot(path="step3_post_clicked.png") # تیسرا قدم
            
            time.sleep(10)
            
            # کامیابی
            posts.pop(0)
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
            print("Done.")
            
        except Exception as e:
            page.screenshot(path="error_final.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    post_to_facebook_group()
