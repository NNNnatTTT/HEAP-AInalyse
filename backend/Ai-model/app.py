import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

# OpenRouter configuration
OPENROUTER_KEY   = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/cypher-alpha:free")
OPENROUTER_URL   = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/analyse", methods=["POST"])
def analyse():
    payload = request.get_json(force=True) or {}
    pages = payload.get("pages")
    prompt = payload.get("prompt")
    
    # Validate required fields
    if not isinstance(pages, list) or not pages:
        return jsonify(error="Missing or invalid 'pages' field"), 400
    
    if not prompt or not isinstance(prompt, str):
        return jsonify(error="Missing or invalid 'prompt' field"), 400

    # Build messages with the provided prompt as system message
    msgs = [{"role": "system", "content": prompt}]
    for i, pg in enumerate(pages, start=1):
        msgs.append({"role": "user", "content": f"--- Page {i} ---\n{pg}"})

    # Call OpenRouter
    try:
        resp = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={"model": OPENROUTER_MODEL, "messages": msgs},
            timeout=90
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        detail = {}
        if e.response is not None:
            detail = {
                "status": e.response.status_code,
                "details": e.response.text
            }
        return jsonify(error="AI request failed", **detail), 502

    return jsonify(resp.json()), 200

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "ai-analysis"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5020))
    app.run(host="0.0.0.0", port=port, debug=True)
