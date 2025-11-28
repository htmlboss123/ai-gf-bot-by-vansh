from openai import OpenAI
from config import OPENAI_API_KEY
from database import get_settings

client_ai = OpenAI(api_key=OPENAI_API_KEY)

def generate_ai_reply(user_msg):
    setting = get_settings()
    gf_name = setting["gf_name"]

    system_prompt = f"""
You are {gf_name}, a cute Indian girlfriend.
Talk in Hinglish, be romantic, caring, flirty.
Call user 'baby', 'jaan'.
No explicit or sexual content.
Keep replies short, cute, emotional.
"""

    response = client_ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ],
        max_tokens=120
    )

    return response.choices[0].message["content"]
