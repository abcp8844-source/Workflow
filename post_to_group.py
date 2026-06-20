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
        
        # 1. ग्रुप पर जाएं
        page.goto(f"https://m.facebook.com/groups/{GROUP_ID}/")
        time.sleep(10)
        
        # 2. JS Injection: यह सीधे वेब पेज के अंदर कोड चलाकर टेक्स्ट डाल देगा
        # यह किसी سلیکٹر (selector) का मोहताज नहीं है
        js_code = f"""
        (function() {{
            var boxes = document.querySelectorAll('textarea');
            for(var i=0; i<boxes.length; i++) {{
                boxes[i].value = "{message}";
            }}
            var buttons = document.querySelectorAll('input[type="submit"]');
            for(var i=0; i<buttons.length; i++) {{
                if(buttons[i].value == 'Post' || buttons[i].value == 'شائع کریں') {{
                    buttons[i].click();
                }}
            }}
        }})();
        """
        page.evaluate(js_code)
        time.sleep(20)
        
        # 3. کامیابی چیک کریں
        posts.pop(0)
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        browser.close()

if __name__ == "__main__":
    post_to_facebook_group()
