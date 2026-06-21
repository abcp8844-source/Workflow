import os
import json
import time
from playwright.sync_api import sync_playwright

PAGE_ID = os.environ.get("PAGE_ID")
STATE_PATH = "auth_state.json"
FILE_PATH = "pending_posts.json"

def post_to_facebook_page():
    if not os.path.exists(FILE_PATH): return
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try: posts = json.load(f)
        except: return
    if not posts: return

    current_post = posts[0]
    message = (
        f"🌟 {current_post.get('title', '').upper()}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Hello everyone,\n\n"
        "Excellence meets opportunity. At our platform, we believe that your career deserves nothing less than verified precision. We filter out the noise and the scams to bring you only the most authentic, globally verified opportunities.\n\n"
        "We don’t just list jobs; we curate a pathway to professional growth. Experience the standard of verified excellence today.\n\n"
        f"🔗 Apply Here: {current_post.get('link', '')}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "#CareerExcellence #VerifiedOpportunities #GlobalHiring #ProfessionalGrowth "
        "#JobSearch #VerifiedJobs #CareerPath #TopJobs2026"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=STATE_PATH,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(f"https://www.facebook.com/{PAGE_ID}")
        
        # کل والا تیز طریقہ
        time.sleep(15) 
        try:
            page.click("[role='button']:has-text('Write something')")
            time.sleep(5)
            editor = page.locator("[role='dialog'] [role='textbox']")
            editor.fill(message) # ٹائپنگ کی بجائے فل کرنا تیز ہے
            time.sleep(3)
            page.click("[role='dialog'] [role='button']:has-text('Post')")
            time.sleep(10)
            
            posts.pop(0)
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            page.screenshot(path="error.png")
        browser.close()

if __name__ == "__main__":
    post_to_facebook_page()
