from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os
import requests


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

@app.route('/save_analsis', methods=['POST'])
def upload_document():
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Get additional metadata from form data
        title = request.form.get('title', file.filename)
        description = request.form.get('description', '')
        category = request.form.get('category', 'general')
        tags = request.form.get('tags', '')
        
        # Validate file type
        if not allowed_file(file.filename, file.mimetype):
            return jsonify({
                "error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}"
            }), 400
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Read file content
        file_content = file.read()
        file_size = len(file_content)
        
        # Upload file to Supabase Storage
        storage_path = f"documents/{unique_filename}"
        
        # Upload to Supabase storage bucket (assuming bucket name is 'documents')
        storage_response = supabase.storage.from_('documents').upload(
            path=storage_path,
            file=file_content,
            file_options={
                "content-type": file.mimetype,
                "cache-control": "3600"
            }
        )
        
        if hasattr(storage_response, 'error') and storage_response.error:
            return jsonify({"error": f"Failed to upload file: {storage_response.error}"}), 500
        
        # Get public URL for the uploaded file
        public_url = supabase.storage.from_('documents').get_public_url(storage_path)
        
        # Store document metadata in database
        document_data = {
            "title": title,
            "description": description,
            "original_filename": original_filename,
            "stored_filename": unique_filename,
            "file_path": storage_path,
            "file_size": file_size,
            "mime_type": file.mimetype,
            "category": category,
            "tags": tags,
            "public_url": public_url,
            "uploaded_at": datetime.utcnow().isoformat(),
            "active": True
        }
        
        # Insert document record into database
        db_response = (
            supabase
            .from_('documents')
            .insert(document_data)
            .execute()
        )
        
        return jsonify({
            "message": "Document uploaded successfully",
            "document_id": db_response.data[0]['id'] if db_response.data else None,
            "filename": original_filename,
            "stored_filename": unique_filename,
            "file_size": file_size,
            "public_url": public_url,
            "data": db_response.data
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9697,debug=True)