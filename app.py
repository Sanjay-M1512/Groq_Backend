from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq_client import generate_text
import re

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

# ===============================
# CORS CONFIGURATION (ALLOW ALL)
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],       # Allow all HTTP methods
    allow_headers=["*"],       # Allow all headers (including Authorization)
)

# ===============================
# REQUEST MODEL
# ===============================
class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 200


# ===============================
# TECHNICAL PROMPT FILTER
# ===============================
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


# ===============================
# HEALTH CHECK
# ===============================
@app.get("/")
def health():
    return {"status": "ZOE coding backend running"}


# ===============================
# CHAT ENDPOINT
# ===============================
@app.post("/chat")
def chat(req: ChatRequest):
    # Block non-technical prompts
    if not is_technical_prompt(req.prompt):
        return {
            "response": "I am ZOE, designed exclusively for coding and problem-solving tasks. Please ask a technical question."
        }

    try:
        # Call Groq API
        result = generate_text(req.prompt, req.max_tokens)
        return {"response": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
