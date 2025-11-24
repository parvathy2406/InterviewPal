from groq import Groq
from config.config import Config

def groq_answer(prompt):
    if not Config.GROQ_API_KEY:
        return "[ERROR] No GROQ_API_KEY set in environment."

    client = Groq(api_key=Config.GROQ_API_KEY)

    resp = client.chat.completions.create(
        model="llama3-8b-8192",  
        messages=[
            {"role": "system", "content": "You are a helpful interview preparation coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return resp.choices[0].message.content
