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
        posts = json.load(f)
    if not posts: return

    current_post = posts[0]
    # آپ کی مطلوبہ میسج ترتیب
    message = f"{current_post['title']}\n\nExcellence meets opportunity. At our platform, we believe that your career deserves nothing less than verified precision. We filter out the noise and the scams to bring you only the most authentic, globally verified opportunities.\n\nWe don’t just list jobs; we curate a pathway to professional growth. Experience the standard of verified excellence today.\n\n👉 Apply Here: {current_post['link']}\n\n#CareerExcellence #VerifiedOpportunities #GlobalHiring #ProfessionalGrowth #JobSearch #VerifiedJobs #CareerPath #TopJobs2026 #GlobalCareers #AuthenticOpportunities"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # یہاں موبائل یوزر ایجنٹ سیٹ کر رہے ہیں تاکہ وہ آپ کی کوکیز سے میچ کرے
        context = browser.new_context(
            storage_state=STATE_PATH,
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        )
        page = context.new_page()
        
        # موبائل ورژن پر نیویگیٹ کریں
        page.goto(f"https://m.facebook.com/groups/{GROUP_ID}/", wait_until="networkidle")
        time.sleep(15)

        try:
            # پوسٹ باکس ڈھونڈنا (موبائل ویو پر)
            page.locator("div[class*='_55wr']").first.click()
            time.sleep(5)
            
            # ٹائپ کریں
            page.keyboard.type(message)
            time.sleep(5)
            
            # پوسٹ بٹن (موبائل پر 'Post' بٹن)
            page.locator("button[value='Post']").click()
            time.sleep(20)
            
            # کامیابی کے بعد فائل اپ ڈیٹ
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
