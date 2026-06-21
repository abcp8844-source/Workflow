import os
import json
import requests

# آپ کی پیج آئی ڈی
PAGE_ID = "514947098373834"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
FILE_PATH = "pending_posts.json"

def post_to_facebook_page():
    if not os.path.exists(FILE_PATH):
        return
    
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try:
            posts = json.load(f)
        except:
            return
            
    if not posts:
        return

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

    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        posts.pop(0)
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print("Post successful!")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    post_to_facebook_page()
