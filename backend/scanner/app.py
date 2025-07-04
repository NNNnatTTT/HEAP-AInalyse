from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
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

@app.route('/scan', methods=['POST'])
def scan_document():
    # receive file
    # Scan to text
    # Save text to DB
    # Call uploader API to send doc to DSS
    # 
    if 'file' not in request.files:
        return jsonify({"error": "No file in request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save file temporarily for fitz
    temp_path = f"/tmp/{file.filename}"
    file.save(temp_path)

    # Extract text from PDF
    extracted_text = ""
    try:
        doc = fitz.open(temp_path)
        for page in doc:
            extracted_text += page.get_text()
        doc.close()
    except Exception as e:
        return jsonify({"error": f"Failed to extract text: {str(e)}"}), 500

    original_filename = secure_filename(file.filename)
    file_extension = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    # Upload file to Supabase Storage
    storage_path = f"documents/{unique_filename}"
        
    # # Send scanned text to it's OWN supabase database
    # try:
    #     bucket_name = "documents"  # Supabase bucket
    #     with open(temp_path, "rb") as f:
    #         response = supabase.storage.from_(bucket_name).upload(
    #             filename, f)
    #         if response.get("error"):
    #             return jsonify({"error": "Failed to upload to Supabase"}), 500
    # except Exception as e:
    #     return jsonify({"error": f"Supabase upload error: {str(e)}"}), 500

    # Upload to Supabase storage bucket (assuming bucket name is 'documents')
    storage_response = supabase.storage.from_('documents').upload(
        path=storage_path,
        # file=file_content,
        file_options={
            "content-type": file.mimetype,
            "cache-control": "3600"
        }
    )
    
    if hasattr(storage_response, 'error') and storage_response.error:
        return jsonify({"error": f"Failed to upload file: {storage_response.error}"}), 500
    
    # Send original file to DSS
    STORAGE_SERVICE_URL = "http://<DSS_HOST>:<port>/upload_document"
    try:
        with open(temp_path, 'rb') as f:
            storage_response = requests.post(STORAGE_SERVICE_URL, files={"file": f})
            if storage_response.status_code != 201:
                return jsonify({"error": "Failed to store file in storage service"}), 500
    except Exception as e:
        return jsonify({"error": f"Storage service error: {str(e)}"}), 500

    # Return extracted text
    return jsonify({"text": extracted_text})



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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9697,debug=True)