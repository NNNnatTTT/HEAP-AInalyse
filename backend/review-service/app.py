import os, json
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import requests
import logging

app = Flask(__name__)
CORS(app)
# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



# Load your one-off prompt template
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "prompts", "review-prompt.json")) as f:
    prompt_data = json.load(f)
USER_PROMPT = prompt_data["prompt"]

AI_MODEL_URL = os.getenv("AI_MODEL_URL", "http://ai-model:5020")

@app.route('/review-service', methods=['POST'])
def review_document():
    data = request.get_json(force=True) or {}
    pages = data.get("pages")
    if not isinstance(pages, list) or not pages:
        return jsonify(error="No pages provided"), 400

    # Simply hand off pages + your single prompt to the ai-model service:
    try:
        ai_resp = requests.post(
            f"{AI_MODEL_URL}/ai",
            json={
                "pages":  pages,
                "prompt": USER_PROMPT
            },
            timeout=90
        )
        ai_resp.raise_for_status()
    except requests.RequestException as e:
        detail = {}
        if e.response is not None:
            detail = {
                "status":  e.response.status_code,
                "details": e.response.text
            }
        return jsonify(error="AI-model failed", **detail), 502
    
    print("📝 review-service raw response:", ai_resp.json())
    ai_payload = ai_resp.json()
    app.logger.info(f"📝 review-service raw response: {ai_payload}")

    # Return the AI-model’s JSON straight back
    return jsonify(ai_resp.json()), 200

if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run(host='0.0.0.0', port=5003, debug=True, use_reloader=False)
    # app.run(host='0.0.0.0', port=5003, debug=True)



# @app.route('/review_document/<document_id>', methods=['POST'])
# def review_doc(document_name):
#     # Get text for review
#     # review based on training from correct contracts
#     # Discrepencies are highlighted and the location
#         # Of the fucked up lines are saved in JSON in analysis results
#         # To be used by suggestions



#     # From document-storage-service, NOT upload service
#     DSS_getDocByID_url = f"http://localhost:<port>/get_document/{document_name}"

#     try:
#         response = requests.get(DSS_getDocByID_url)
#         if response.status_code == 200:
#             data = response.json()
#             document = data["document"]
#             # Review pipelining

#         else:
#             print(f"Error: {response.status_code} - {response.text}")
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
