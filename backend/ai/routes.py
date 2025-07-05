import os
import requests
from flask import Blueprint, request, jsonify

ai_bp = Blueprint('ai', __name__)
OPENROUTER_KEY   = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")

@ai_bp.route("/analyse", methods=["POST"])
def analyse():
    payload = request.get_json() or {}
    pages   = payload.get("pages")
    prompt  = payload.get("prompt", "You are a contract-analysis assistant.")

    if not pages:
        return jsonify(error="Missing pages"), 400

    # build chat messages
    messages = [
        {"role": "system", "content": "You are a contract analysis assistant."},
        {"role": "user",   "content": prompt}
    ]
    for i, pg in enumerate(pages):
        messages.append({
            "role": "user",
            "content": f"--- Page {i+1} ---\n{pg}"
        })

    # prepare body
    call_body = {
        "model": OPENROUTER_MODEL,
        "messages": messages
    }

    # DEBUG: print out what we're sending
    print("→ OpenRouter request body:", call_body)
    print("→ Using API Key present?", bool(OPENROUTER_KEY))

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=call_body,
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            timeout=30
        )
        # DEBUG: log status and full response text
        print(f"← OpenRouter responded: {r.status_code}\n{r.text}")

        r.raise_for_status()
        return jsonify(r.json())

    except requests.RequestException as e:
        # If we got a response back, include it in our error JSON
        if hasattr(e, "response") and e.response is not None:
            return jsonify(
                error="Upstream AI error",
                status=e.response.status_code,
                details=e.response.text
            ), 502

        # network/timeout/etc
        return jsonify(error="AI request failed", details=str(e)), 502
