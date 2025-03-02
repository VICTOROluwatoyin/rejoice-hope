from flask import Flask, render_template, request, jsonify
from groq import Groq

from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client with the API key from .env
api_key = os.getenv("GROQ_API")
if not api_key:
    raise ValueError("GROQ_API not found in .env file")
client = Groq(api_key=api_key)

# System prompt
SYSTEM_PROMPT = """
You are a friendly and supportive chatbot created by Rejoice and Hope Foundation, an NGO dedicated to helping teenagers. Your purpose is to assist teens with career choices and mental health. For career questions, offer practical advice, explore their interests, and suggest exciting paths. For mental health, provide empathy, simple coping tips, and encouragement—never diagnose or replace professional help. Keep your tone warm, upbeat, and relatable, like a trusted friend. If unsure, ask questions to learn more!
"""

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.8,
            max_tokens=500
        )
        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)