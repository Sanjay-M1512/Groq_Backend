import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # 👈 MUST be here

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_text(prompt: str, max_tokens: int = 200):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response.choices[0].message.content
