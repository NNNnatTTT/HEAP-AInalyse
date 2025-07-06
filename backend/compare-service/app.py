from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import requests
import os
import io, uuid, tempfile



app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": ["http://localhost:5173"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}})
# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)




@app.route('/add_session/<modsecyear>', methods=['GET'])
def add_session(modsecyear):
    try:
        # Check which sessions already exist
        existing_sessions = []
        for i in range(1, 13):
            title = f"w{i}"
            response = (
                supabase
                .from_('session')
                .select('*')
                .match({'modsecyear': modsecyear, 'title': title})
                .execute()
            )
            if response.data:
                existing_sessions.append(title)
        
        if len(existing_sessions) == 12:
            return jsonify({"message": "All session records already exist"}), 200
        
        # Create records for sessions that don't exist
        new_sessions = []
        for i in range(1, 13):
            title = f"w{i}"
            if title not in existing_sessions:
                new_sessions.append({
                    "modsecyear": modsecyear, 
                    "title": title, 
                    "active": False
                })
        
        # Insert new sessions into Supabase
        if new_sessions:
            response = (
                supabase
                .from_('session')
                .insert(new_sessions)
                .execute()
            )
            return jsonify({
                "message": f"Added {len(new_sessions)} new sessions. {len(existing_sessions)} sessions already existed.",
                "new_sessions": [s['title'] for s in new_sessions],
                "existing_sessions": existing_sessions,
                "data": response.data
            })
        else:
            return jsonify({"message": "All sessions already exist", "existing_sessions": existing_sessions})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update_active', methods=['POST'])
def update_active():
    try:
        data = request.json
        modsecyear = data.get("modsecyear")
        title = data.get("title")
        active = data.get("active")
        if(active):
            res = (
            supabase
            .from_('session')
            .update({"active": False})
            .match({"modsecyear": modsecyear})
            .execute()
        )  
            

        if modsecyear is None or title is None or active is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Update Supabase record
        response = (
            supabase
            .from_('session')
            .update({"active": active})
            .match({"modsecyear": modsecyear, "title": title})
            .execute()
        )


        return jsonify({"message": "Update successful", "data": response.data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_active', methods=['GET'])
def get_active():
    try:
        session_id = request.args.get("session_id")
        modsecyear = request.args.get("modsecyear")
        title = request.args.get("title")

        if session_id:
            response = (
                supabase
                .from_('session')
                .select("active")
                .eq("session_id", session_id)
                .execute()
            )
        elif modsecyear and title:
            response = (
                supabase
                .from_('session')
                .select("active")
                .match({"modsecyear": modsecyear, "title": title})
                .execute()
            )

        elif modsecyear:
            response = (
                supabase
                .from_('session')
                .select("session_id","title")
                .match({"modsecyear": modsecyear})
                .is_("active", True)
                .execute()
            )
        else:
            return jsonify({"error": "Missing required query parameters"}), 400

        return jsonify({"message": "Query successful", "data": response.data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_session_id', methods=['GET'])
def get_session_id():
    try:
        modsecyear = request.args.get("modsecyear")
        title = request.args.get("title")

        if modsecyear and title:
            response = (
                supabase
                .from_('session')
                .select("session_id")
                .match({"modsecyear": modsecyear, "title": title})
                .execute()
            )
        else:
            return jsonify({"error": "Missing required query parameters"}), 400

        # Check if data exists and return the first element, else return an error
        if response.data:
            return jsonify(response.data[0]), 200
        else:
            return jsonify({"error": "No matching session found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_modsecyear', methods=['GET'])
def get_modsecyear():
    try:
        session_id= request.args.get("session_id")

        if session_id:
            response = (
                supabase
                .from_('session')
                .select("modsecyear")
                .match({"session_id": session_id})
                .execute()
            )
        else:
            return jsonify({"error": "Missing required query parameters"}), 400

        # Check if data exists and return the first element, else return an error
        if response.data:
            return jsonify(response.data[0]), 200
        else:
            return jsonify({"error": "No matching modsecyear found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_all_title/<modsecyear>', methods=['GET'])
def get_all_title(modsecyear):
    try:

        if modsecyear:
            response = (
                supabase
                .from_('session')
                .select("title","session_id")
                .match({"modsecyear": modsecyear})
                .execute()
            )
        else:
            return jsonify({"error": "Missing required query parameters"}), 400

        # Check if data exists and return the first element, else return an error
        data = response.data
        if response:
            return jsonify(data), 200
        else:
            return jsonify({"error": "No matching modsecyear found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Example service URLs (replace with your actual endpoints)
# SCANNER_URL = "SCANNER_URL"
# DOCUMENT_SERVICE = "DOCUMENT_URL"
# AI_SERVICE = "AI_URL"

# @app.route('/upload-service', methods=['POST'])
# def upload_and_process_pdf():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part in the request"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     if not file.filename.lower().endswith('.pdf'):
#         return jsonify({"error": "Only PDF files are allowed"}), 400

#     try:
#         # 1. Send PDF to scanner service
#         scanner_response = requests.post(
#             SCANNER_URL,
#             files={'file': (file.filename, file, 'application/pdf')}
#         )
#         if scanner_response.status_code != 200:
#             return jsonify({"error": "Scanner service error", "details": scanner_response.text}), 500

#         scanner_json = scanner_response.json()

#         # 2. Send scanner output to second service
#         second_response = requests.post(
#             DOCUMENT_SERVICE,
#             json=scanner_json
#         )
#         if second_response.status_code != 200:
#             return jsonify({"error": "Second service error", "details": second_response.text}), 500

#         second_json = second_response.json()

#         # 3. Send second service output to third service
#         third_response = requests.post(
#             AI_SERVICE,
#             json=second_json
#         )
#         if third_response.status_code != 200:
#             return jsonify({"error": "Third service error", "details": third_response.text}), 500

#         final_json = third_response.json()
#         return jsonify(final_json), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

    
    
# This for dashboard actually, unless want to show recent docs list
# @app.route('/upload-service/get-all', methods=['GET'])
# def get_all_documents():

# @app.route('/upload-service/<document_id>', methods=['GET'])
# def get_document(document_id):

# def delete_document(document_id):

# def update_document(document_id):

# --------------------  UPLOAD + SCAN  --------------------
ALLOWED_MIME = {"application/pdf"}

@app.route("/upload-service", methods=["POST"])
def upload_and_scan():
    """
    Receives a PDF from the UI, pipes it to scanner,
    and returns the pages’ text as JSON.
    """
    file = request.files.get("file")
    if not file or file.mimetype not in ALLOWED_MIME:
        return jsonify(error="Please upload a PDF"), 400

    # read bytes once so we can both forward & (optionally) keep them
    pdf_bytes = file.read()

    # --- call scanner ----------------------------------------
    try:
        scan_resp = requests.post(
            "http://scanner:5004/scan_document",   # container name or docker-compose service
            files={"file": ("upload.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
            timeout=6000,
        )
        scan_resp.raise_for_status()
    except requests.RequestException as e:
        return jsonify(error="scanner failed", details=str(e)), 502

    ocr_res = scan_resp.json()        # {"message": "...", "text": "…"}
    pages_text = ocr_res.get("text", "")

    # split each “--- Page N ---” section into a list
    pages = [p.strip() for p in pages_text.split("\n--- Page") if p.strip()]
    return jsonify(pages=pages, page_count=len(pages))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
