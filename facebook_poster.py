import os
import json
import time
import random
from playwright.sync_api import sync_playwright

GROUP_ID = "1403757117731031"
STATE_PATH = "auth_state.json"
FILE_PATH = "pending_posts.json"

def post_to_facebook_group():
    # 1. Read from pending list using your exact original logic
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

    # Verify if the one-time saved session file exists
    if not os.path.exists(STATE_PATH):
        print("Authentication state file missing. Please run the initial login script first.")
        return

    # 2. Browser Automation using the saved session and slow strategic timing
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Open browser context utilizing the saved data file (never logs in again)
        context = browser.new_context(
            storage_state=STATE_PATH,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        group_url = f"https://www.facebook.com/groups/{GROUP_ID}"
        print(f"Navigating directly to Facebook Group: {group_url}")
        page.goto(group_url)
        
        # Human Delay 1: Wait 35-45 seconds immediately after landing on the group page
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
            
            # Human Delay 2: Wait 12-18 seconds after opening the text editor before typing
            post_box_wait = random.randint(12, 18)
            print(f"Post box opened. Waiting for {post_box_wait} seconds before typing...")
            time.sleep(post_box_wait)
            
            editor_selector = "[role='dialog'] [role='textbox']"
            page.focus(editor_selector)
            
            # Human Delay 3: Typing character by character slowly
            print("Typing the message slowly to mimic real human fingers...")
            for char in message:
                page.type(editor_selector, char)
                time.sleep(random.uniform(0.03, 0.09))
            
            # Brief pause after typing finishes before clicking post
            time.sleep(5)
            
            post_button_selector = "[role='dialog'] [role='button']:has-text('Post')"
            page.click(post_button_selector)
            
            # Human Delay 4: Wait a full 25 seconds for uploading to finish properly
            print("Submitting post to the group... Waiting 25 seconds for completion.")
            time.sleep(25)
            
            print("Successfully posted to Facebook Group using the permanent saved session!")
            
            # 3. Keep original file maintenance logic on success
            posts.pop(0)
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
            print("Post removed from pending list.")
            
            # Refresh session cookies state file in case Facebook updated any details
            context.storage_state(path=STATE_PATH)
            
        except Exception as e:
            print(f"Error during browser automation posting: {e}")
            page.screenshot(path="error_screenshot.png")
            
        browser.close()

if __name__ == "__main__":
    post_to_facebook_group()
