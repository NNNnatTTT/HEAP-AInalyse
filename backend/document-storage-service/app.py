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
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get('uuid') or payload.get('sub')
    except:
        return None

@app.route('/upload_json', methods=['POST'])
def upload_json():
    try:
        user_uuid = get_current_user()
        if not user_uuid:
            return jsonify({"error": "Unable to identify user"}), 400

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        filename = data.get('filename')
        description = data.get('description', '')  # Default to empty string
        file_content = data.get('content')

        if not filename or not file_content:
            return jsonify({"error": "Missing filename or content"}), 400

        # Store data directly in your files table
        file_record = {
            "user_id": user_uuid,      # Matches your user_id column
            "filename": filename,       # Matches your filename column
            "file": file_content,       # Matches your file JSONB column
            "description": description  # Matches your description column
        }
        
        db_response = supabase.from_('files').insert(file_record).execute()

        return jsonify({
            "message": "JSON file stored successfully",
            "id": db_response.data[0]['id'] if db_response.data else None,
            "filename": filename,
            "data": db_response.data[0] if db_response.data else None
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
            .eq('user_id', user_uuid)  # Use user_id column name
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
            .eq('user_id', user_uuid)  # Use user_id column name
            .order('id', desc=True)    # Order by id since no created_at column
            .execute()
        )
        return jsonify(response.data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/file/<fileID>', methods=['PUT'])
def update_file(fileID):
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Check if file exists and belongs to user
        existing = (
            supabase
            .from_('files')
            .select('id')
            .eq('id', fileID)
            .eq('user_id', user_uuid)
            .execute()
        )
        
        if not existing.data:
            return jsonify({"error": "File not found"}), 404

        # Prepare update data
        update_data = {}
        if 'filename' in data:
            update_data['filename'] = data['filename']
        if 'file' in data:
            update_data['file'] = data['file']
        if 'description' in data:
            update_data['description'] = data['description']

        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400

        # Update the file
        response = (
            supabase
            .from_('files')
            .update(update_data)
            .eq('id', fileID)
            .eq('user_id', user_uuid)
            .execute()
        )

        return jsonify({
            "message": "File updated successfully",
            "data": response.data[0] if response.data else None
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/file/<fileID>', methods=['DELETE'])
def delete_file(fileID):
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        # Delete the file record
        response = (
            supabase
            .from_('files')
            .delete()
            .eq('id', fileID)
            .eq('user_id', user_uuid)
            .execute()
        )
        
        if not response.data:
            return jsonify({"error": "File not found"}), 404

        return jsonify({"message": "File deleted successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4567, debug=True)
