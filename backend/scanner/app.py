from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from pdf2image import convert_from_bytes
from PIL import Image 
import pytesseract    
import os
import requests
import fitz
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
import io

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

# @app.route('/scan', methods=['POST'])
# def scan_document():
#     # receive file
#     # Scan to text
#     # Save text to DB
#     # Call uploader API to send doc to DSS
#     # 
#     if 'file' not in request.files:
#         return jsonify({"error": "No file in request"}), 400

# @app.route('/add_session/<modsecyear>', methods=['GET'])
# def add_session(modsecyear):
#     try:
#         doc = fitz.open(temp_path)
#         for page in doc:
#             extracted_text += page.get_text()
#         doc.close()
#     except Exception as e:
#         return jsonify({"error": f"Failed to extract text: {str(e)}"}), 500

#     original_filename = secure_filename(file.filename)
#     file_extension = original_filename.rsplit('.', 1)[1].lower()
#     unique_filename = f"{uuid.uuid4()}.{file_extension}"

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
    

@app.route('/api/compare', methods=['POST'])
def compare_documents():
    try:
        # 1) grab both files from the incoming request
        fileA = request.files.get('fileA')
        fileB = request.files.get('fileB')
        if not fileA or not fileB:
            return jsonify({"error": "Both fileA and fileB are required"}), 400

        # helper to reuse your existing scan logic via an internal POST
        def do_scan(f):
            files = {'file': (f.filename, f.stream, f.mimetype)}
            r = requests.post('http://localhost:9697/scan_document', files=files)
            r.raise_for_status()
            return r.json()

        # 2) scan both PDFs
        resultA = do_scan(fileA)
        resultB = do_scan(fileB)

        # 3) send the two JSON blobs to your AI/Gemini service
        ai_payload = {
          "mode": "compare",
          "contractData": {
            "contract1": resultA,
            "contract2": resultB
          }
        }
        ai_resp = requests.post(
          'http://localhost:3000/api/gemini',
          json=ai_payload
        )
        ai_resp.raise_for_status()

        # 4) return the AI’s response as JSON
        return jsonify(ai_resp.json())

    except requests.HTTPError as e:
        return jsonify({"error": f"Upstream service error: {e}"}), 502
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
    
#     # Upload file to Supabase Storage
#     storage_path = f"documents/{unique_filename}"
        
#     # # Send scanned text to it's OWN supabase database
#     # try:
#     #     bucket_name = "documents"  # Supabase bucket
#     #     with open(temp_path, "rb") as f:
#     #         response = supabase.storage.from_(bucket_name).upload(
#     #             filename, f)
#     #         if response.get("error"):
#     #             return jsonify({"error": "Failed to upload to Supabase"}), 500
#     # except Exception as e:
#     #     return jsonify({"error": f"Supabase upload error: {str(e)}"}), 500

#     # Upload to Supabase storage bucket (assuming bucket name is 'documents')
#     storage_response = supabase.storage.from_('documents').upload(
#         path=storage_path,
#         # file=file_content,
#         file_options={
#             "content-type": file.mimetype,
#             "cache-control": "3600"
#         }
#     )
    
#     if hasattr(storage_response, 'error') and storage_response.error:
#         return jsonify({"error": f"Failed to upload file: {storage_response.error}"}), 500
    
#     # Send original file to DSS
#     STORAGE_SERVICE_URL = "http://<DSS_HOST>:<port>/upload_document"
#     try:
#         with open(temp_path, 'rb') as f:
#             storage_response = requests.post(STORAGE_SERVICE_URL, files={"file": f})
#             if storage_response.status_code != 201:
#                 return jsonify({"error": "Failed to store file in storage service"}), 500
#     except Exception as e:
#         return jsonify({"error": f"Storage service error: {str(e)}"}), 500

#     # Return extracted text
#     return jsonify({"text": extracted_text})
    
@app.route('/scan_document', methods=['POST'])
def scan_document():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        filename = file.filename.lower()
        extracted_text = ""

        if filename.endswith('.pdf'):
            # Convert PDF pages to images
            images = convert_from_bytes(file.read())
            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image)
                extracted_text += f"\n--- Page {i+1} ---\n{text}"
        else:
            # Assume it's an image
            image = Image.open(file.stream)
            extracted_text = pytesseract.image_to_string(image)
        
        print(f"Extracted text: {extracted_text}")

        return jsonify({"message": "OCR successful", "text": extracted_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9697,debug=True)