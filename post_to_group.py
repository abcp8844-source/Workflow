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
        print("Pending file not found.")
        return

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try:
            posts = json.load(f)
        except json.JSONDecodeError:
            print("Empty or invalid JSON file.")
            return

    if not posts:
        print("No pending posts available.")
        return

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

    if not os.path.exists(STATE_PATH):
        print("Authentication state file missing. Run login script first.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        context = browser.new_context(
            storage_state=STATE_PATH,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        group_url = f"https://www.facebook.com/groups/{GROUP_ID}"
        print(f"Navigating to Facebook Group: {group_url}")
        page.goto(group_url)
        
        initial_wait = random.randint(35, 45)
        print(f"Simulating human reading behavior. Waiting for {initial_wait} seconds...")
        time.sleep(initial_wait)
        
        try:
            post_box_selectors = [
                "text=Write something...",
                "span:has-text('Write something...')",
                "[role='button']:has-text('Write something...')"
            ]
            
            clicked = False
            for selector in post_box_selectors:
                if page.locator(selector).is_visible():
                    page.click(selector)
                    clicked = True
                    break
            
            if not clicked:
                page.click("[role='main'] [role='button']")
            
            post_box_wait = random.randint(12, 18)
            print(f"Post box opened. Waiting for {post_box_wait} seconds before typing...")
            time.sleep(post_box_wait)
            
            editor_selector = "[role='dialog'] [role='textbox']"
            page.focus(editor_selector)
            
            print("Typing the message slowly...")
            for char in message:
                page.type(editor_selector, char)
                time.sleep(random.uniform(0.03, 0.09))
            
            time.sleep(5)
            
            post_button_selector = "[role='dialog'] [role='button']:has-text('Post')"
            page.click(post_button_selector)
            
            print("Submitting post to the group... Waiting 25 seconds for completion.")
            time.sleep(25)
            
            print("Successfully posted to Facebook Group!")
            
            posts.pop(0)
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
            print("Post removed from pending list.")
            
            context.storage_state(path=STATE_PATH)
            
        except Exception as e:
            print(f"Error during browser automation posting: {e}")
            page.screenshot(path="error_screenshot.png")
            
        browser.close()

if __name__ == "__main__":
    post_to_facebook_group()
