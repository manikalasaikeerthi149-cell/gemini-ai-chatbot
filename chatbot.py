from flask import Flask, render_template, request, jsonify
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Enable Google Search tool
google_search_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[google_search_tool],
    temperature=1.0
)

# Create chat session with memory
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=config
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        message = data["message"]

        response = chat.send_message(message)

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "reply": f"Error: {str(e)}"
        })

@app.route("/clear", methods=["POST"])
def clear():
    global chat

    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=config
    )

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)