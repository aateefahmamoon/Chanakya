from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


def detect_language(text):
    # Simple detection stub - extend with langdetect if you want real detection
    return "English"


def load_scheme_documents(folder_path="schemes"):
    all_text = ""
    if not os.path.exists(folder_path):
        print(f"⚠️ Folder '{folder_path}' does not exist.")
        return ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
                all_text += file.read() + "\n"
    return all_text.strip()


scheme_context = load_scheme_documents()


def get_gemini_response(user_query):
    model = genai.GenerativeModel("gemini-2.5-flash")

    user_lang = detect_language(user_query)

    prompt = f"""
You are YojanaSaathi, an assistant that helps Indian citizens understand government welfare schemes.

Use the following scheme information to answer clearly, simply, and in the same language as the user's question.

The user has asked their question in **{user_lang}**, so respond only in **{user_lang}**, using natural expressions in that language. Do not switch languages mid-answer.

Context:
{scheme_context}

Question:
{user_query}

Answer:
"""

    response = model.generate_content(prompt)
    return response.text.strip()


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get("query", "")
    if not user_msg:
        return jsonify({"answer": "No question given."})
    answer = get_gemini_response(user_msg)
    return jsonify({"answer": answer})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8501)
