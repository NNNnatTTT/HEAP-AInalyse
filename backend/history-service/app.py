from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import jwt

app = Flask(__name__)

# Configure CORS properly for preflight requests
CORS(app)

# Service URLs from environment variables
DOCUMENT_STORAGE_SERVICE_URL = os.getenv('DOCUMENT_STORAGE_SERVICE_URL', 'http://document-storage-service:5009')
ANALYSE_RESULTS_SERVICE_URL = os.getenv('ANALYSE_RESULTS_SERVICE_URL', 'http://analyse-results:5008')

def get_current_user():
    """Extract user UUID from JWT with detailed logging"""
    if request.method == "OPTIONS":
        return None
        
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        app.logger.warning("No Authorization header found")
        return None
    
    token = auth_header.split(' ')[1]
    try:
        # Decode without verification (Kong already validated)
        payload = jwt.decode(token, options={"verify_signature": False})
        
        # Detailed logging
        app.logger.info(f"JWT Payload: {payload}")
        app.logger.info(f"Available keys: {list(payload.keys())}")
        
        # Extract user ID using your auth service logic
        user_id = payload.get('uuid') or payload.get('sub')
        app.logger.info(f"Extracted user ID: {user_id}")
        app.logger.info(f"User ID type: {type(user_id)}")
        
        if not user_id:
            app.logger.error("No user ID found in JWT payload")
            return None
            
        return str(user_id)  # Ensure it's a string
        
    except Exception as e:
        app.logger.error(f"JWT decode error: {e}")
        return None

def get_documents_by_user_uuid(user_uuid):
    """Retrieve all documents for a specific user UUID from document storage service"""
    try:
        resp = requests.get(
            f"{DOCUMENT_STORAGE_SERVICE_URL}/user/{user_uuid}/files",
            timeout=30
        )
        resp.raise_for_status()
        response_data = resp.json()
        
        # Extract the files array from the response
        return response_data.get('files', [])
    except requests.RequestException as e:
        app.logger.error(f"Document storage error: {e}")
        raise

def get_document_from_storage(document_id):
    """Retrieve document from document storage service"""
    try:
        auth_header = request.headers.get('Authorization')
        headers = {}
        if auth_header:
            headers['Authorization'] = auth_header
        
        resp = requests.get(
            f"{DOCUMENT_STORAGE_SERVICE_URL}/file/{document_id}",
            headers=headers,
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        app.logger.error(f"Document storage error: {e}")
        raise

def get_analysis_results(file_id):
    """Retrieve analysis results from analyse results service using file_id"""
    try:
        resp = requests.get(
            f"{ANALYSE_RESULTS_SERVICE_URL}/results/{file_id}",
            timeout=30
        )
        if resp.status_code == 200:
            response_data = resp.json()
            # Return the results array from the new endpoint response
            return response_data.get('results', [])
        elif resp.status_code == 404:
            # No analysis results found for this file
            return None
        else:
            resp.raise_for_status()
    except requests.RequestException as e:
        app.logger.error(f"Analysis results service error: {e}")
        return None

@app.route('/history', methods=['GET', 'OPTIONS'])
def get_user_history():
    """Get all documents for the current user with their analysis results"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        # Use the new endpoint to get documents by user UUID
        documents = get_documents_by_user_uuid(user_uuid)
        
        enhanced_documents = []
        for doc in documents:
            file_id = doc.get('id')  # Use the file ID from document storage
            analysis_results = get_analysis_results(file_id)
            
            enhanced_doc = {
                "document": doc,
                "analysis_results": analysis_results,
                "has_analysis": analysis_results is not None and len(analysis_results) > 0
            }
            
            enhanced_documents.append(enhanced_doc)
        
        return jsonify({
            "user_id": user_uuid,
            "total_documents": len(enhanced_documents),
            "documents": enhanced_documents
        }), 200
        
    except requests.RequestException as e:
        return jsonify({"error": "Failed to retrieve user history", "details": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/history/<document_id>', methods=['GET', 'OPTIONS'])
def get_document_history(document_id):
    """Get specific document with its analysis results"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        document = get_document_from_storage(document_id)
        analysis_results = get_analysis_results(document_id)
        
        return jsonify({
            "document": document,
            "analysis_results": analysis_results,
            "has_analysis": analysis_results is not None and len(analysis_results) > 0
        }), 200
        
    except requests.RequestException as e:
        if "404" in str(e):
            return jsonify({"error": "Document not found"}), 404
        return jsonify({"error": "Failed to retrieve document history", "details": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/history/analysis/<document_id>', methods=['GET', 'OPTIONS'])
def get_document_analysis_only(document_id):
    """Get only the analysis results for a specific document"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        document = get_document_from_storage(document_id)
        analysis_results = get_analysis_results(document_id)
        
        if not analysis_results or len(analysis_results) == 0:
            return jsonify({"error": "No analysis results found for this document"}), 404
        
        return jsonify({
            "document_id": document_id,
            "analysis_results": analysis_results
        }), 200
        
    except requests.RequestException as e:
        if "404" in str(e):
            return jsonify({"error": "Document not found"}), 404
        return jsonify({"error": "Failed to retrieve analysis results", "details": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/history/summary', methods=['GET', 'OPTIONS'])
def get_history_summary():
    """Get summary statistics of user's document history"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        # Use the new endpoint to get documents by user UUID
        documents = get_documents_by_user_uuid(user_uuid)
        
        total_documents = len(documents)
        documents_with_analysis = 0
        
        for doc in documents:
            file_id = doc.get('id')  # Use the file ID from document storage
            analysis_results = get_analysis_results(file_id)
            if analysis_results and len(analysis_results) > 0:
                documents_with_analysis += 1
        
        return jsonify({
            "user_id": user_uuid,
            "total_documents": total_documents,
            "documents_with_analysis": documents_with_analysis,
            "documents_without_analysis": total_documents - documents_with_analysis,
            "analysis_completion_rate": (documents_with_analysis / total_documents * 100) if total_documents > 0 else 0
        }), 200
        
    except requests.RequestException as e:
        return jsonify({"error": "Failed to retrieve history summary", "details": str(e)}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "history-service"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5030, debug=True)
