import os
import json
import requests

PAGE_ID = "514947098373834"
ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
FILE_PATH = "pending_posts.json"

def post_to_facebook():
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

    
    page_url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
    
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }

    try:
        response = requests.post(page_url, data=payload)
        res_data = response.json()

        if "id" in res_data:
            print(f"Successfully posted to Facebook Page! Post ID: {res_data['id']}")
            # پوسٹ کامیاب ہونے پر لسٹ سے ہٹائیں
            posts.pop(0)
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
            print("Post removed from pending list.")
        else:
            print(f"Facebook API Error: {res_data}")
    except Exception as e:
        print(f"Error during posting: {e}")

if __name__ == "__main__":
    post_to_facebook()
