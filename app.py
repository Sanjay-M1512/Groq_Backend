from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from groq_client import generate_text

load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 200

@app.get("/")
def health():
    return {"status": "Groq API backend running"}

@app.post("/chat")
def chat(req: ChatRequest):
    return {
        "response": generate_text(req.prompt, req.max_tokens)
    }
