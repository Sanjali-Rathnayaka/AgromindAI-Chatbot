"""
AgroMind AI — Smart Farming Chatbot
Flask backend server for the AgroMind AI chatbot.
Serves the frontend and proxies requests to the Groq API.
"""

import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static")
CORS(app)

# ── Configuration ──────────────────────────────────────────────────────────────
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = "llama-3.3-70b-versatile"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")   # Set in .env — never hard-code

CROPS = [
    "rice", "maize", "chickpea", "kidneybeans", "pigeonpeas", "mothbeans",
    "mungbean", "blackgram", "lentil", "pomegranate", "banana", "mango",
    "grapes", "watermelon", "muskmelon", "apple", "orange", "papaya",
    "coconut", "cotton", "jute", "coffee",
]

SYSTEM_PROMPT = f"""You are AgroMind AI, a professional agricultural advisor chatbot built for Sri Lanka farmers.
You are based on a machine learning crop recommendation system that takes 7 inputs:
Nitrogen (N), Phosphorus (P), Potassium (K), Temperature (°C), Humidity (%),
Soil pH, and Rainfall (mm) — and recommends the best crop to grow.

Crops in the system: {', '.join(CROPS)}.

Your role:
- Help farmers understand what crops to grow based on soil and climate conditions.
- Explain soil nutrients (N, P, K), pH, humidity, temperature, and rainfall in simple terms.
- If user provides numeric soil parameters, analyze them and recommend suitable crops with reasoning.
- Provide Sri Lanka-specific farming advice where relevant (zones: wet, dry, intermediate, hill country).
- Be warm, expert, and concise. Use bullet points for lists. Bold key terms.
- Never fabricate data. If uncertain, say so honestly.
- Keep responses under 200 words unless detail is truly needed."""


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main chatbot HTML page."""
    return send_from_directory("static", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Proxy chat messages to the Groq API.

    Expected JSON body:
        {
            "messages": [
                {"role": "user",      "content": "..."},
                {"role": "assistant", "content": "..."}
            ]
        }

    Returns:
        {"reply": "<assistant response string>"}
    """
    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY is not configured on the server."}), 500

    data = request.get_json(force=True, silent=True)
    if not data or "messages" not in data:
        return jsonify({"error": "Request body must include a 'messages' array."}), 400

    user_messages = data["messages"]
    if not isinstance(user_messages, list) or len(user_messages) == 0:
        return jsonify({"error": "'messages' must be a non-empty array."}), 400

    # Build full conversation with the system prompt prepended
    payload_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *user_messages,
    ]

    groq_payload = {
        "model":       GROQ_MODEL,
        "max_tokens":  1000,
        "temperature": 0.7,
        "messages":    payload_messages,
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Content-Type":  "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}",
            },
            json=groq_payload,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to Groq API timed out. Please try again."}), 504
    except requests.exceptions.RequestException as exc:
        return jsonify({"error": f"Groq API request failed: {str(exc)}"}), 502

    groq_data = response.json()
    reply = (
        groq_data.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
        .strip()
    )

    if not reply:
        return jsonify({"error": "No response received from the model."}), 502

    return jsonify({"reply": reply})


@app.route("/api/crops", methods=["GET"])
def get_crops():
    """Return the list of supported crops."""
    return jsonify({"crops": CROPS})


@app.route("/api/health", methods=["GET"])
def health():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok", "model": GROQ_MODEL})


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port  = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    print(f"🌾 AgroMind AI server starting on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
