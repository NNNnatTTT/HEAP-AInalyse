import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": ["http://localhost:5173"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}})

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


@app.route('/suggestions/<result_id>', methods=['POST'])
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
    payload = {
        "analysis": analysis,
        "prompt_key": prompt_key,
        "prompt": prompt
    }
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



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from supabase import create_client, Client
# import os
# import requests


# app = Flask(__name__)
# CORS(app, resources={r"/*": {
#     "origins": ["http://localhost:5173"],
#     "methods": ["GET", "POST", "OPTIONS"],
#     "allow_headers": ["Content-Type"]
# }})
# # Supabase credentials
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# def get_analsis_results():
#     get_analsis_results_URL = f"http://localhost:<port>/get_results"
#     try:
#         response = requests.post(get_analsis_results_URL)
#         if response.status_code == 200:
#             data = response.json()
#             results = data["results"]
#             # Review pipelining
            
#         else:
#             print(f"Error: {response.status_code} - {response.text}")
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
#     return results



# @app.route('/suggest', methods=['POST'])
# def get_suggestions():
#     # results = get_analsis_results()
#     # Based on results, generate changes to rectify the issues

#     get_analsis_results_URL = f"http://localhost:<port>/get_results"
#     try:
#         response = requests.post(get_analsis_results_URL)
#         if response.status_code == 200:
#             data = response.json()
#             results = data["results"]
#             # Review pipelining





            
#         else:
#             print(f"Error: {response.status_code} - {response.text}")
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500








# # Evoke review when successful upload
# # Review has a POST api called here
# def review_doc(document_name):
#     # Some POST api
#     RS_review_url = f"http://<DSS_HOST>:<port>/review_document/<{document_name}>"
#     try:
#         response = requests.post(RS_review_url)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/upload-service', methods=['POST'])
# def upload_document():
#     # Call document-storage-service upload
#     # Pass document into this service review_doc()
#     # review_doc() calls review service to continue
#     DSS_upload_url = f"http://<DSS_HOST>:<port>/upload_document"

#     try:
#         response = requests.post(DSS_upload_url)
#         if response.status_code == 200:
#             data = response.json()
#             document = data["stored_filename"]
#             # Review pipelining
#             review_doc(document) # Is string ig
            
#         else:
#             print(f"Error: {response.status_code} - {response.text}")
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

    
    
# # This for dashboard actually, unless want to show recent docs list
# # @app.route('/upload-service/get-all', methods=['GET'])
# # def get_all_documents():

# # @app.route('/upload-service/<document_id>', methods=['GET'])
# # def get_document(document_id):

# # def delete_document(document_id):

# # def update_document(document_id):


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=9697,debug=True)