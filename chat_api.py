from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
# replace with your Gemini API key
api_key = os.getenv("AIzaSyC9DQfoaCnWauHmgwJ9khxlAVfs-Im5iRk")
genai.configure(api_key=api_key)


def get_gemini_response(user_query):
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"You are YojanaSaathi, an assistant. Question: {user_query}\nAnswer:"
    response = model.generate_content(prompt)
    return response.text.strip()


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get("query", "")
    answer = get_gemini_response(
        user_msg) if user_msg else "No question given."
    return jsonify({"answer": answer})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8501)
