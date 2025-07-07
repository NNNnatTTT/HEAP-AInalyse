# app.py

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_wrapper import OpenRouterWrapper
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

<<<<<<< Updated upstream
# ← your OpenRouter creds must be set in the environment:
OPENROUTER_KEY   = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/cypher-alpha:free")
OPENROUTER_URL   = "https://openrouter.ai/api/v1/chat/completions"

# Pre-defined prompts keyed however you like:
PROMPT_TEMPLATES = {
    "contractAnalysis": (
        "You are a contract analysis assistant. "
        "Identify suspicious clauses, key obligations, and potential risks."
    ),
    "riskAssessment": (
        "You are a legal risk assessment assistant. "
        "Evaluate any financial or compliance risks in this contract."
    ),
    "keyTerms": (
        "You are a summarization assistant. "
        "Extract the important dates, amounts, and obligations."
    ),
    "recommendations": (
        "You are a contract improvement assistant. "
        "Suggest ways to strengthen this contract and mitigate risks."
    )
}

@app.route("/analyse", methods=["POST"])
def analyse():
    payload    = request.get_json(force=True) or {}
    pages      = payload.get("pages")
    prompt_key = payload.get("promptKey")
    override   = payload.get("prompt")

    # Validate
    if not isinstance(pages, list) or not pages:
        return jsonify(error="Missing or invalid 'pages'"), 400

    # Choose system prompt
    if override:
        system = override
    else:
        system = PROMPT_TEMPLATES.get(prompt_key, PROMPT_TEMPLATES["contractAnalysis"])

    # Build messages
    msgs = [{"role": "system", "content": system}]
    for i, pg in enumerate(pages, start=1):
        msgs.append({"role": "user", "content": f"--- Page {i} ---\n{pg}"})

    # Call OpenRouter
    try:
        resp = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type":  "application/json"
            },
            json={"model": OPENROUTER_MODEL, "messages": msgs},
            timeout=90
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        detail = {}
        if e.response is not None:
            detail = {
                "status":  e.response.status_code,
                "details": e.response.text
            }
=======
# initialize once
ai_client = OpenRouterWrapper()

@app.route("/ai", methods=["POST"])
def ai():
    body   = request.get_json(force=True) or {}
    pages  = body.get("pages")
    prompt = body.get("prompt")

    # 1) validate
    if not isinstance(pages, list) or not pages:
        return jsonify(error="Missing or invalid 'pages'"), 400
    if not prompt or not isinstance(prompt, str):
        return jsonify(error="Missing or invalid 'prompt'"), 400

    # 2) delegate to wrapper
    try:
        result = ai_client.generate(pages=pages, system_prompt=prompt)
    except requests.RequestException as e:
        detail = {"status": e.response.status_code, "details": e.response.text} if e.response else {}
>>>>>>> Stashed changes
        return jsonify(error="AI request failed", **detail), 502
    except RuntimeError as e:
        return jsonify(error=str(e)), 500

    # 3) return
    return jsonify(result), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5020))
    app.run(host="0.0.0.0", port=port, debug=True)


<<<<<<< Updated upstream
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




# @app.route('/add_session/<modsecyear>', methods=['GET'])
# def add_session(modsecyear):
#     try:
#         # Check which sessions already exist
#         existing_sessions = []
#         for i in range(1, 13):
#             title = f"w{i}"
#             response = (
#                 supabase
#                 .from_('session')
#                 .select('*')
#                 .match({'modsecyear': modsecyear, 'title': title})
#                 .execute()
#             )
#             if response.data:
#                 existing_sessions.append(title)
        
#         if len(existing_sessions) == 12:
#             return jsonify({"message": "All session records already exist"}), 200
        
#         # Create records for sessions that don't exist
#         new_sessions = []
#         for i in range(1, 13):
#             title = f"w{i}"
#             if title not in existing_sessions:
#                 new_sessions.append({
#                     "modsecyear": modsecyear, 
#                     "title": title, 
#                     "active": False
#                 })
        
#         # Insert new sessions into Supabase
#         if new_sessions:
#             response = (
#                 supabase
#                 .from_('session')
#                 .insert(new_sessions)
#                 .execute()
#             )
#             return jsonify({
#                 "message": f"Added {len(new_sessions)} new sessions. {len(existing_sessions)} sessions already existed.",
#                 "new_sessions": [s['title'] for s in new_sessions],
#                 "existing_sessions": existing_sessions,
#                 "data": response.data
#             })
#         else:
#             return jsonify({"message": "All sessions already exist", "existing_sessions": existing_sessions})
            
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/update_active', methods=['POST'])
# def update_active():
#     try:
#         data = request.json
#         modsecyear = data.get("modsecyear")
#         title = data.get("title")
#         active = data.get("active")
#         if(active):
#             res = (
#             supabase
#             .from_('session')
#             .update({"active": False})
#             .match({"modsecyear": modsecyear})
#             .execute()
#         )  
            

#         if modsecyear is None or title is None or active is None:
#             return jsonify({"error": "Missing required fields"}), 400

#         # Update Supabase record
#         response = (
#             supabase
#             .from_('session')
#             .update({"active": active})
#             .match({"modsecyear": modsecyear, "title": title})
#             .execute()
#         )


#         return jsonify({"message": "Update successful", "data": response.data})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/get_active', methods=['GET'])
# def get_active():
#     try:
#         session_id = request.args.get("session_id")
#         modsecyear = request.args.get("modsecyear")
#         title = request.args.get("title")

#         if session_id:
#             response = (
#                 supabase
#                 .from_('session')
#                 .select("active")
#                 .eq("session_id", session_id)
#                 .execute()
#             )
#         elif modsecyear and title:
#             response = (
#                 supabase
#                 .from_('session')
#                 .select("active")
#                 .match({"modsecyear": modsecyear, "title": title})
#                 .execute()
#             )

#         elif modsecyear:
#             response = (
#                 supabase
#                 .from_('session')
#                 .select("session_id","title")
#                 .match({"modsecyear": modsecyear})
#                 .is_("active", True)
#                 .execute()
#             )
#         else:
#             return jsonify({"error": "Missing required query parameters"}), 400

#         return jsonify({"message": "Query successful", "data": response.data})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/get_session_id', methods=['GET'])
# def get_session_id():
#     try:
#         modsecyear = request.args.get("modsecyear")
#         title = request.args.get("title")

#         if modsecyear and title:
#             response = (
#                 supabase
#                 .from_('session')
#                 .select("session_id")
#                 .match({"modsecyear": modsecyear, "title": title})
#                 .execute()
#             )
#         else:
#             return jsonify({"error": "Missing required query parameters"}), 400

#         # Check if data exists and return the first element, else return an error
#         if response.data:
#             return jsonify(response.data[0]), 200
#         else:
#             return jsonify({"error": "No matching session found"}), 404

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# @app.route('/get_modsecyear', methods=['GET'])
# def get_modsecyear():
#     try:
#         session_id= request.args.get("session_id")

#         if session_id:
#             response = (
#                 supabase
#                 .from_('session')
#                 .select("modsecyear")
#                 .match({"session_id": session_id})
#                 .execute()
#             )
#         else:
#             return jsonify({"error": "Missing required query parameters"}), 400

#         # Check if data exists and return the first element, else return an error
#         if response.data:
#             return jsonify(response.data[0]), 200
#         else:
#             return jsonify({"error": "No matching modsecyear found"}), 404

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/get_all_title/<modsecyear>', methods=['GET'])
# def get_all_title(modsecyear):
#     try:

#         if modsecyear:
#             response = (
#                 supabase
#                 .from_('session')
#                 .select("title","session_id")
#                 .match({"modsecyear": modsecyear})
#                 .execute()
#             )
#         else:
#             return jsonify({"error": "Missing required query parameters"}), 400

#         # Check if data exists and return the first element, else return an error
#         data = response.data
#         if response:
#             return jsonify(data), 200
#         else:
#             return jsonify({"error": "No matching modsecyear found"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=9697,debug=True)
=======

# import os
# import requests
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

# # OpenRouter configuration
# OPENROUTER_KEY   = os.getenv("OPENROUTER_API_KEY")
# OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/cypher-alpha:free")
# OPENROUTER_URL   = "https://openrouter.ai/api/v1/chat/completions"

# @app.route("/analyse", methods=["POST"])
# def analyse():
#     payload = request.get_json(force=True) or {}
#     pages = payload.get("pages")
#     prompt = payload.get("prompt")
    
#     # Validate required fields
#     if not isinstance(pages, list) or not pages:
#         return jsonify(error="Missing or invalid 'pages' field"), 400
    
#     if not prompt or not isinstance(prompt, str):
#         return jsonify(error="Missing or invalid 'prompt' field"), 400

#     # Build messages with the provided prompt as system message
#     msgs = [{"role": "system", "content": prompt}]
#     for i, pg in enumerate(pages, start=1):
#         msgs.append({"role": "user", "content": f"--- Page {i} ---\n{pg}"})

#     # Call OpenRouter
#     try:
#         resp = requests.post(
#             OPENROUTER_URL,
#             headers={
#                 "Authorization": f"Bearer {OPENROUTER_KEY}",
#                 "Content-Type": "application/json"
#             },
#             json={"model": OPENROUTER_MODEL, "messages": msgs},
#             timeout=90
#         )
#         resp.raise_for_status()
#     except requests.RequestException as e:
#         detail = {}
#         if e.response is not None:
#             detail = {
#                 "status": e.response.status_code,
#                 "details": e.response.text
#             }
#         return jsonify(error="AI request failed", **detail), 502

#     return jsonify(resp.json()), 200

# @app.route("/health", methods=["GET"])
# def health_check():
#     return jsonify({"status": "healthy", "service": "ai-analysis"}), 200

# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 5020))
#     app.run(host="0.0.0.0", port=port, debug=True)
>>>>>>> Stashed changes
