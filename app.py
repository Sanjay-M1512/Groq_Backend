from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from groq_client import generate_text
import re

load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 200


# Simple technical keyword check
def is_technical_prompt(text: str) -> bool:
    keywords = [
        "code", "python", "java", "c++", "javascript", "react", "fastapi",
        "error", "bug", "exception", "traceback", "api", "sql", "database",
        "algorithm", "data", "machine learning", "ai", "model",
        "cloud", "aws", "docker", "kubernetes", "nginx", "linux",
        "function", "class", "object", "debug", "compile", "runtime"
    ]

    text = text.lower()
    return any(keyword in text for keyword in keywords)


@app.get("/")
def health():
    return {"status": "ZOE coding backend running"}


@app.post("/chat")
def chat(req: ChatRequest):
    if not is_technical_prompt(req.prompt):
        return {
            "response": "I am ZOE, designed exclusively for coding and problem-solving tasks. Please ask a technical question."
        }

    try:
        result = generate_text(req.prompt, req.max_tokens)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
