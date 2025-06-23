College Info Chatbot
A chatbot that answers queries about colleges using NLP, built with FastAPI, Hugging Face Transformers, and a Tailwind CSS frontend.
Project Structure
college-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── utils.py
│   │   └── colleges.json
│   ├── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── scripts.js
├── data/
│   ├── prepare_data.py
│   ├── training_data.json
│   ├── fine_tune_model.py
├── README.md
└── .gitignore

Setup

Clone the repository:git clone <your-repo-url>
cd college-chatbot


Set up virtual environment:python -m venv venv
source venv/bin/activate


Install backend dependencies:cd backend
pip install -r requirements.txt


Run the backend:uvicorn app.main:app --reload


Run the frontend:cd ../frontend
python -m http.server 3000


Open http://localhost:3000 in a browser.

Deployment

Backend: Hosted on Render
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT


Frontend: Hosted on Netlify
Base Directory: frontend
Publish Directory: frontend



Optional: Fine-Tune NLP Model

Run data/prepare_data.py to generate training_data.json.
Run data/fine_tune_model.py on a GPU-enabled environment.
Update backend/app/main.py to use the fine-tuned model.

Example Queries

"What are the courses at CITM?"
"Convener quota fee at KLEF?"
"Tell me about SRM University."
