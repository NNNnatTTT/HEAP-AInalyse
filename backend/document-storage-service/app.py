from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from supabase import create_client, Client
import os
import requests
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": ["http://localhost:5173"],
    "methods": ["GET", "POST", "OPTIONS", "DELETE"],
    "allow_headers": ["Content-Type"]
}})

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Allowed file extensions and MIME types
ALLOWED_EXTENSIONS = {
    'pdf': 'application/pdf',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'doc': 'application/msword',
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpg',
    'png': 'image/png',
    'gif': 'image/gif'
}

ALLOWED_MIME_TYPES = {
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword',
    'image/jpeg',
    'image/jpg',
    'image/png',
    'image/gif'
}

def allowed_file(filename, mimetype):
    """Check if the file extension and MIME type are allowed"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return (extension in ALLOWED_EXTENSIONS and 
            mimetype in ALLOWED_MIME_TYPES and
            ALLOWED_EXTENSIONS[extension] == mimetype)

@app.route('/upload_document', methods=['POST'])
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

@app.route('/get_document/<document_id>', methods=['GET'])
def get_document(document_id):
    try:
        # Get document metadata from database
        response = (
            supabase
            .from_('documents')
            .select('*')
            .eq('id', document_id)
            .eq('active', True)
            .execute()
        )
        
        if not response.data:
            return jsonify({"error": "Document not found"}), 404
        
        document = response.data[0]
        
        # Check if user wants to download the file
        download = request.args.get('download', 'false').lower() == 'true'
        
        if download:
            try:
                # Download file from Supabase storage
                file_response = supabase.storage.from_('documents').download(document['file_path'])
                
                if not file_response:
                    return jsonify({"error": "Failed to download file from storage"}), 500
                
                # Create file-like object
                file_obj = io.BytesIO(file_response)
                
                return send_file(
                    file_obj,
                    mimetype=document['mime_type'],
                    as_attachment=True,
                    download_name=document['original_filename']
                )
                
            except Exception as e:
                return jsonify({"error": f"Failed to retrieve file: {str(e)}"}), 500
        else:
            # Return document metadata only
            return jsonify({
                "message": "Document retrieved successfully",
                "document": document
            }), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_documents', methods=['GET'])
def get_documents():
    try:
        # Get query parameters for filtering
        category = request.args.get('category')
        search = request.args.get('search')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Build query
        query = supabase.from_('documents').select('*').eq('active', True)
        
        # Apply filters
        if category:
            query = query.eq('category', category)
        
        if search:
            query = query.or_(f'title.ilike.%{search}%,description.ilike.%{search}%,tags.ilike.%{search}%')
        
        # Apply pagination
        query = query.range(offset, offset + limit - 1)
        
        # Order by upload date (newest first)
        query = query.order('uploaded_at', desc=True)
        
        response = query.execute()
        
        return jsonify({
            "message": "Documents retrieved successfully",
            "documents": response.data,
            "count": len(response.data)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_document/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    try:
        # Get document metadata first
        response = (
            supabase
            .from_('documents')
            .select('*')
            .eq('id', document_id)
            .eq('active', True)
            .execute()
        )
        
        if not response.data:
            return jsonify({"error": "Document not found"}), 404
        
        document = response.data[0]
        
        # Delete file from storage
        try:
            supabase.storage.from_('documents').remove([document['file_path']])
        except Exception as storage_error:
            print(f"Warning: Failed to delete file from storage: {storage_error}")
        
        # Mark document as inactive in database (soft delete)
        update_response = (
            supabase
            .from_('documents')
            .update({"active": False})
            .eq('id', document_id)
            .execute()
        )
        
        return jsonify({
            "message": "Document deleted successfully",
            "document_id": document_id
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_document/<document_id>', methods=['PUT'])
def update_document(document_id):
    try:
        data = request.json
        
        # Fields that can be updated
        updatable_fields = ['title', 'description', 'category', 'tags']
        update_data = {}
        
        for field in updatable_fields:
            if field in data:
                update_data[field] = data[field]
        
        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400
        
        # Update document metadata
        response = (
            supabase
            .from_('documents')
            .update(update_data)
            .eq('id', document_id)
            .eq('active', True)
            .execute()
        )
        
        if not response.data:
            return jsonify({"error": "Document not found or update failed"}), 404
        
        return jsonify({
            "message": "Document updated successfully",
            "document": response.data[0]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9697, debug=True)
