import os
import json
import time
import random
from playwright.sync_api import sync_playwright

GROUP_ID = "1403757117731031"
STATE_PATH = "auth_state.json"
FILE_PATH = "pending_posts.json"

def post_to_facebook_group():
    if not os.path.exists(FILE_PATH):
        return
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)
    if not posts:
        return

    current_post = posts[0]
    message = f"{current_post['title']}\n\nExcellence meets opportunity. At our platform, we believe that your career deserves nothing less than verified precision. We filter out the noise and the scams to bring you only the most authentic, globally verified opportunities.\n\nWe don’t just list jobs; we curate a pathway to professional growth. Experience the standard of verified excellence today.\n\n👉 Apply Here: {current_post['link']}\n\n#CareerExcellence #VerifiedOpportunities #GlobalHiring #ProfessionalGrowth #JobSearch #VerifiedJobs #CareerPath #TopJobs2026 #GlobalCareers #AuthenticOpportunities"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=STATE_PATH, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        page.goto(f"https://www.facebook.com/groups/{GROUP_ID}")
        page.wait_for_load_state("networkidle")
        time.sleep(random.randint(20, 30))

        try:
            post_box = page.locator("div[role='button'][aria-label*='Write something']")
            if post_box.count() > 0:
                post_box.first.click()
            else:
                page.locator("div.x1i10hfl").first.click()
            
            time.sleep(10)
            page.keyboard.type(message)
            time.sleep(5)
            page.locator("div[aria-label='Post'][role='button']").click()
            time.sleep(30)
            
            posts.pop(0)
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            page.screenshot(path="error.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    post_to_facebook_group()
