import os
import json
import time
import random
from playwright.sync_api import sync_playwright

GROUP_ID = "1403757117731031"
STATE_PATH = "auth_state.json"
FILE_PATH = "pending_posts.json"

def post_to_facebook_group():
    # فائل کا وجود چیک کریں
    if not os.path.exists(FILE_PATH):
        print("Pending file not found.")
        return

    # ترتیب کے ساتھ پوسٹ پڑھیں
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)

    if not posts:
        print("No pending posts available.")
        return

    # پہلی پوسٹ اٹھائیں (آپ کی پرانی ترتیب کے مطابق)
    current_post = posts[0]
    title = current_post.get("title", "")
    link = current_post.get("link", "")

    # آپ کا وہ مخصوص برانڈ کا انداز جو آپ کو پسند ہے
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

    # پلے رائٹ شروع کریں
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=STATE_PATH)
        page = context.new_page()
        
        # گروپ کا لنک
        page.goto(f"https://www.facebook.com/groups/{GROUP_ID}")
        time.sleep(random.randint(35, 45))
        
        # پوسٹ باکس ڈھونڈنا
        try:
            page.click("[role='button']:has-text('Write something...')")
            time.sleep(15)
            
            # ٹائپ کرنا
            editor_selector = "[role='dialog'] [role='textbox']"
            page.focus(editor_selector)
            page.keyboard.type(message) # یہ زیادہ تیزی سے کام کرے گا
            
            time.sleep(5)
            page.click("[role='dialog'] [role='button']:has-text('Post')")
            time.sleep(25)
            
            print("Successfully posted!")

            # اب لاجک: کامیاب پوسٹ کے بعد لسٹ سے نکال دیں
            posts.pop(0)
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
            print("Post removed from pending list.")
            
        except Exception as e:
            print(f"Error: {e}")
            
        browser.close()

if __name__ == "__main__":
    post_to_facebook_group()
