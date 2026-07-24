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
            f"{title}\n\n"
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
        Rewrite and enhance the following job/travel post to make it extremely engaging, professional, and trending on Facebook.
        
        Original Title: {title}
        Original Description: {description}
        Link: {link}
        Date: {formatted_date}
        
        Guidelines:
        - IMPORTANT: Do NOT use big star symbols (like 🌟) anywhere in the text.
        - Use clean, relevant, and appealing emojis (like 🌐 for website, 🔗 for links, 📅 for dates, etc.) to make it look structured and professional.
        - Make the hook catchy and exciting.
        - Keep the apply link and visit website link clearly visible with their respective emojis.
        - Add a set of high-performing, trending hashtags at the end related to jobs, travel, visas, and career growth.
        - Return only the final formatted post text ready to publish.
        """
        
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini Error: {e}, using default fallback.")
        return (
            f"{title}\n\n"
            f"{description}\n\n"
            f"🔗 Apply Here: {link}\n\n"
            f"{formatted_date}"
            "🌐 Visit: zunexhire.com\n\n"
            "#CareerExcellence #VerifiedOpportunities #GlobalHiring #ProfessionalGrowth "
            "#JobSearch #VerifiedJobs #CareerPath #job #visa #travel #zunexhire #TopJobs2026"
        )

def post_to_facebook():
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

    url_page = f"https://graph.facebook.com/v25.0/{PAGE_ID}/photos"
    payload_page = {
        "message": final_message,
        "url": post_image,
        "access_token": ACCESS_TOKEN
    }
    
    response = requests.post(url_page, data=payload_page)
    
    if response.status_code == 200:
        print("Post successful on Page with perfect formatting!")
        posts.pop(0)
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print("pending_posts.json updated successfully!")
    else:
        print(f"Error on Page Post: {response.text}")

if __name__ == "__main__":
    post_to_facebook()
