import os
import json
import requests
from datetime import datetime

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
    
    raw_date = current_post.get('timestamp', '')
    formatted_date = ""
    if raw_date:
        try:
            date_obj = datetime.strptime(raw_date.split('T')[0], '%Y-%m-%d')
            formatted_date = f"📅 DATE: {date_obj.strftime('%d-%m-%Y')}\n"
        except:
            pass

    post_title = current_post.get('title', '')
    post_description = current_post.get('description', '')
    post_link = current_post.get('link', '')

    message = (
        f"{formatted_date}"
        f"🌟 {post_title.upper()}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{post_description}\n\n"
        f"🔗 Apply Here: {post_link}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🌐 zunexhire.com\n\n"
        "#CareerExcellence #VerifiedOpportunities #GlobalHiring #ProfessionalGrowth "
        "#JobSearch #VerifiedJobs #CareerPath #job #visa #travel #zunexhire #TopJobs2026"
    )

    url = f"https://graph.facebook.com/v25.0/{PAGE_ID}/feed"
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
