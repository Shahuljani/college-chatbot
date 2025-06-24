import json
import re
import difflib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS for Netlify frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://apaskvidya.netlify.app"],  # Replace with your frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load training data (Q&A)
with open("training_data.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

# Load college data (for fallback)
try:
    with open("colleges.json", "r", encoding="utf-8") as f:
        college_data = json.load(f)
except:
    college_data = []

# Model for input
class ChatRequest(BaseModel):
    message: str

# Utils
def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def find_closest_question(user_question):
    questions = [normalize(pair["question"]) for pair in qa_data]
    match = difflib.get_close_matches(normalize(user_question), questions, n=1, cutoff=0.5)
    return match[0] if match else None

def get_answer_for_question(matched_q):
    for pair in qa_data:
        if normalize(pair["question"]) == matched_q:
            return pair["answer"]
    return None

def extract_college_info(message):
    norm_msg = normalize(message)
    for college in college_data:
        code = normalize(college.get("Institution_code", ""))
        name = normalize(college.get("Name of the Institution", ""))
        if code in norm_msg or name in norm_msg:
            return format_college_info(college)
    return None

def format_college_info(college):
    try:
        return (
            f"Here are the details for **{college['Name of the Institution']}**:\n"
            f"📍 Address: {college['Address1']}, {college['Address2']}, {college['District']}, {college['State']}, PIN: {college['Pin Code']}\n"
            f"🎓 Courses Offered: {', '.join(college['No of courses available in the college'])}\n"
            f"💰 Convener Quota Fee: {college['Annual Fee (Convener Quota)']}\n"
            f"💼 Management Quota Fee: {college['Annual Fee (Management Quota)']}\n"
            f"📈 Placement Percentage: {college['Percentage of Placement']}%\n"
            f"📞 Contact: {college['Phone No. of Head of Instt.']} / {college['Alternate Mobile']}\n"
            f"🏛️ Affiliated To: {college['Affiliated to']}\n"
            f"⭐ Rating: {college['Rating']}"
        )
    except:
        return "College data is incomplete, but we'll improve this soon!"

# Root route
@app.get("/")
def root():
    return {"message": "College Chatbot API is running."}

# Main chatbot route
@app.post("/chat")
async def chat(request: ChatRequest):
    user_question = request.message.strip()

    # Step 1: Match question from training set
    best_match = find_closest_question(user_question)
    if best_match:
        answer = get_answer_for_question(best_match)
        if answer:
            return {"response": answer}

    # Step 2: Match college name/code for full info
    fallback_info = extract_college_info(user_question)
    if fallback_info:
        return {"response": fallback_info}

    # Step 3: Friendly default fallback
    return {
        "response": (
            "🤖 Sorry, I couldn’t find an exact answer to that.\n\n"
            "You can ask me things like:\n"
            "• What is the convener quota fee at BEC?\n"
            "• Tell me about ABIT\n"
            "• Show placement details of ADTP\n\n"
            "I’m here to help with any college-related queries! 🎓"
        )
    }
