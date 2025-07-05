import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import jwt
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_current_user():
    """Extract user UUID from JWT (Kong already validated it)"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    try:
        # Skip signature verification since Kong already validated
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get('uuid') or payload.get('sub')
    except:
        return None

@app.route('/upload_json', methods=['POST'])
def upload_json():
    try:
        # Get user ID (Kong ensures valid JWT)
        user_uuid = get_current_user()
        if not user_uuid:
            return jsonify({"error": "Unable to identify user"}), 400

        # Parse JSON body
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        filename = data.get('filename')
        description = data.get('description')
        file_content = data.get('content')

        if not filename or not file_content:
            return jsonify({"error": "Missing filename or content"}), 400

        # Store JSON as file in Supabase Storage
        storage_path = f"{user_uuid}/{filename}.json"  # User-specific path
        file_bytes = json.dumps(file_content, ensure_ascii=False, indent=2).encode('utf-8')

        storage_response = supabase.storage.from_('files').upload(
            path=storage_path,
            file=file_bytes,
            file_options={
                "content-type": "application/json",
                "cache-control": "3600"
            }
        )

        if hasattr(storage_response, 'error') and storage_response.error:
            return jsonify({"error": f"Failed to upload file: {storage_response.error}"}), 500

        public_url = supabase.storage.from_('files').get_public_url(storage_path)

        # Store metadata in Supabase database
        file_metadata = {
            "filename": filename,
            "description": description,
            "uuid": user_uuid,
            "file_path": storage_path,
            "public_url": public_url,
            "uploaded_at": datetime.utcnow().isoformat(),
            "active": True
        }
        
        db_response = supabase.from_('files').insert(file_metadata).execute()

        return jsonify({
            "message": "JSON file uploaded successfully",
            "id": db_response.data[0]['id'] if db_response.data else None,
            "filename": filename,
            "public_url": public_url,
            "data": db_response.data
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/file/<fileID>', methods=['GET'])
def get_file(fileID):
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        response = (
            supabase
            .from_('files')
            .select('*')
            .eq('id', fileID)
            .eq('uuid', user_uuid)
            .single()
            .execute()
        )
        
        if response.data is None:
            return jsonify({"error": "File not found"}), 404
            
        return jsonify(response.data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files', methods=['GET'])
def get_all_files():
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        response = (
            supabase
            .from_('files')
            .select('*')
            .eq('uuid', user_uuid)
            .order('uploaded_at', desc=True)
            .execute()
        )
        return jsonify(response.data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/file/<fileID>', methods=['DELETE'])
def delete_file(fileID):
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        # Get file to check ownership
        response = (
            supabase
            .from_('files')
            .select('*')
            .eq('id', fileID)
            .eq('uuid', user_uuid)
            .single()
            .execute()
        )
        
        if response.data is None:
            return jsonify({"error": "File not found"}), 404

        # Delete from storage and database
        file_record = response.data
        supabase.storage.from_('files').remove([file_record['file_path']])
        supabase.from_('files').delete().eq('id', fileID).execute()

        return jsonify({"message": "File deleted successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4567, debug=True)  # Use port from Kong config
