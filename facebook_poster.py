import os
import json
import requests

PAGE_ID = "514947098373834"
ACCESS_TOKEN = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")
FILE_PATH = "pending_posts.json"  # آپ کی پینڈنگ فائل کا نام

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

    # لسٹ میں سے سب سے پہلی پوسٹ اٹھائیں
    current_post = posts[0]
    title = current_post.get("title", "")
    link = current_post.get("link", "")

    # فیس بک کے لیے خوبصورت ٹیکسٹ فارمیٹ تیار کرنا
    message = f"{title}\n\n👉 Apply Here: {link}"

    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }

    try:
        response = requests.post(url, data=payload)
        res_data = response.json()

        if "id" in res_data:
            print(f"Successfully posted to Facebook! Post ID: {res_data['id']}")
            
            # پوسٹ کامیاب ہونے پر اسے لسٹ سے حذف کریں
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
