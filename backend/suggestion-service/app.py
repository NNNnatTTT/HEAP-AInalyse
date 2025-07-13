import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# — Environment variable checks —
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL and/or SUPABASE_KEY environment variables")

AI_MODEL_URL = os.getenv("AI_MODEL_URL", "http://ai-model:5020")
if not AI_MODEL_URL:
    raise RuntimeError("Missing AI_MODEL_URL environment variable")

# — Initialize Supabase client —
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# — Load prompt templates (optional) —
BASE = os.path.dirname(os.path.abspath(__file__))
prompts_path = os.path.join(BASE, "prompts", "review-prompt.json")
if os.path.exists(prompts_path):
    with open(prompts_path) as f:
        prompt_data = json.load(f)
else:
    prompt_data = {}
    app.logger.warning("Prompt template file not found at %s", prompts_path)


@app.route('/<result_id>', methods=['POST'])
def make_suggestion(result_id):
    # 0. Validate JSON body
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    prompt_key = body.get("prompt_key")
    # Use canned prompt if available, else fall back to raw prompt
    prompt = prompt_data.get(prompt_key) if prompt_key else None
    if not prompt:
        prompt = body.get("prompt")

    # 1. Fetch the analysis result
    try:
        resp = (
            supabase
            .from_('analyse_results')
            .select('*')
            .eq('id', result_id)
            .execute()
        )
    except Exception as e:
        app.logger.error("Supabase query error: %s", e)
        return jsonify({"error": "Database query failed"}), 500

    if not resp.data:
        return jsonify({"error": "Analysis result not found"}), 404

    analysis = resp.data[0]

    # 2. Prepare payload for AI model
    payload =[{
        "analysis": analysis,
        "prompt_key": prompt_key,
        "prompt": prompt
    }]
    app.logger.debug("Payload to AI model: %s", payload)

    # 3. Send to AI model
    try:
        ai_resp = requests.post(f"{AI_MODEL_URL}/ai", json=payload)
        ai_resp.raise_for_status()
    except requests.HTTPError as http_err:
        status_code = http_err.response.status_code if http_err.response else 500
        app.logger.error("AI model error: %s", http_err)
        return jsonify({"error": f"AI model error: {http_err}"}), status_code
    except Exception as e:
        app.logger.error("Error contacting AI model: %s", e)
        return jsonify({"error": "Failed to contact AI model"}), 500

    # 4. Return AI model’s suggestions
    return jsonify(ai_resp.json()), ai_resp.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)


