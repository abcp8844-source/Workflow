import os
import json
import requests
from datetime import datetime
from google import genai

PAGE_ID = "514947098373834"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") 
FILE_PATH = "pending_posts.json"

def enhance_caption_with_gemini(title, description, link, formatted_date):
    if not GEMINI_API_KEY:
        return (
            f"🌟 {title}\n\n"
            f"{description}\n\n"
            f"🔗 Apply Here: {link}\n\n"
            f"{formatted_date}"
            "🌐 Visit: zunexhire.com\n\n"
            "#CareerExcellence #VerifiedOpportunities #GlobalHiring #ProfessionalGrowth "
            "#JobSearch #VerifiedJobs #CareerPath #job #visa #travel #zunexhire #TopJobs2026"
        )
    
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""
        You are an expert social media manager for 'zunexhire.com'. 
        Rewrite and enhance the following job/travel post to make it extremely engaging, professional, and trending on Facebook to maximize user interaction, likes, and clicks.
        
        Original Title: {title}
        Original Description: {description}
        Link: {link}
        Date: {formatted_date}
        
        Guidelines:
        - Make the hook catchy and exciting.
        - Structure it cleanly with appealing emojis.
        - Keep the apply link and visit website link clearly visible.
        - Add a set of high-performing, trending hashtags at the end related to jobs, travel, visas, and career growth.
        - Return only the final formatted post text ready to publish.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini Error: {e}, using default fallback.")
        return (
            f"🌟 {title}\n\n"
            f"{description}\n\n"
            f"🔗 Apply Here: {link}\n\n"
            f"{formatted_date}"
            "🌐 Visit: zunexhire.com\n\n"
            "#CareerExcellence #VerifiedOpportunities #GlobalHiring #ProfessionalGrowth "
            "#JobSearch #VerifiedJobs #CareerPath #job #visa #travel #zunexhire #TopJobs2026"
        )

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
            formatted_date = f"📅 Date: {date_obj.strftime('%d-%m-%Y')}\n\n"
        except:
            pass

    post_title = current_post.get('title', '')
    post_description = current_post.get('description', '')
    post_link = current_post.get('link', '')
    post_image = current_post.get('image', '')

    final_message = enhance_caption_with_gemini(post_title, post_description, post_link, formatted_date)

    url = f"https://graph.facebook.com/v25.0/{PAGE_ID}/photos"
    payload = {
        "message": final_message,
        "url": post_image,
        "access_token": ACCESS_TOKEN
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        posts.pop(0)
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print("Post successful with Gemini enhancement and image!")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    post_to_facebook_page()
