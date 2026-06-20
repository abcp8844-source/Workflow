import os
import json
import time
import random
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
    title = current_post.get("title", "")
    link = current_post.get("link", "")

    brand_intro = (
        "Hello everyone,\n\n"
        "Excellence meets opportunity. At our platform, we believe that your career deserves nothing less than verified precision. We filter out the noise and the scams to bring you only the most authentic, globally verified opportunities.\n\n"
        "We don’t just list jobs; we curate a pathway to professional growth. Experience the standard of verified excellence today."
    )

    hashtags = (
        "\n\n#CareerExcellence #VerifiedOpportunities #GlobalHiring #ProfessionalGrowth "
        "#JobSearch #VerifiedJobs #CareerPath #TopJobs2026 #GlobalCareers #AuthenticOpportunities"
    )

    message = f"{title}\n\n\n{brand_intro}\n\n👉 Apply Here: {link}{hashtags}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=STATE_PATH,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(f"https://www.facebook.com/groups/{GROUP_ID}")
        time.sleep(random.randint(35, 45))
        
        try:
            post_box = page.locator("[role='button']:has-text('Write something')")
            if post_box.first.is_visible():
                post_box.first.click()
            
            time.sleep(random.randint(12, 18))
            editor = page.locator("[role='dialog'] [role='textbox']")
            editor.focus()
            
            for char in message:
                editor.type(char, delay=random.uniform(0.03, 0.09))
            
            time.sleep(5)
            page.click("[role='dialog'] [role='button']:has-text('Post')")
            time.sleep(25)
            
            posts.pop(0)
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
            
            context.storage_state(path=STATE_PATH)
        except Exception as e:
            page.screenshot(path="error.png")
            
        browser.close()

if __name__ == "__main__":
    post_to_facebook_group()
