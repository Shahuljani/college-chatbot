import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pre-generated training data (Q&A)
with open("training_data.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

# Request format
class ChatRequest(BaseModel):
    message: str

# Utility: Normalize question (basic)
def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())

# Route: Root test
@app.get("/")
def root():
    return {"message": "College Chatbot API is running!"}

# Route: Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    user_question = normalize(request.message)

    # Exact or fuzzy match (can be enhanced with better NLP)
    for pair in qa_data:
        q_normalized = normalize(pair["question"])
        if user_question in q_normalized or q_normalized in user_question:
            return {"response": pair["answer"]}

    return {"response": "Sorry, I couldn't find an answer. Try rephrasing your question or check the college name/code."}
