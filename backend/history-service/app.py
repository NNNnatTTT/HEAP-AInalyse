from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import jwt
import threading
import json

app = Flask(__name__)

# Configure CORS properly for preflight requests
CORS(app)

# Service URLs from environment variables
DOCUMENT_STORAGE_SERVICE_URL = os.getenv('DOCUMENT_STORAGE_SERVICE_URL', 'http://document-storage-service:5009')
ANALYSE_RESULTS_SERVICE_URL = os.getenv('ANALYSE_RESULTS_SERVICE_URL', 'http://analyse-results:5008')
REVIEW_SERVICE_URL = os.getenv('REVIEW_SERVICE_URL', 'http://review-service:5003')

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
        
        # Extract user ID using your auth service logic
        user_id = payload.get('uuid') or payload.get('sub')
        app.logger.info(f"Extracted user ID: {user_id}")
        
        if not user_id:
            app.logger.error("No user ID found in JWT payload")
            return None
            
        return str(user_id)
        
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
        
        # Handle both direct array and wrapped response formats
        if isinstance(response_data, list):
            return response_data
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
            
            # Handle the actual data structure from your analysis service
            if isinstance(response_data, list):
                # Direct list format - process each result
                processed_results = []
                for item in response_data:
                    if isinstance(item, dict) and 'result' in item:
                        # Extract the actual analysis content
                        result_content = item['result']
                        if 'choices' in result_content and len(result_content['choices']) > 0:
                            message_content = result_content['choices'][0].get('message', {}).get('content', '')
                            processed_results.append({
                                'id': item.get('id'),
                                'file_id': item.get('file_id'),
                                'created_at': item.get('created_at'),
                                'content': message_content,
                                'model': result_content.get('model'),
                                'usage': result_content.get('usage')
                            })
                return processed_results
            else:
                # Wrapped format
                return response_data.get('results', [])
                
        elif resp.status_code == 404:
            return None
        else:
            resp.raise_for_status()
            
    except requests.RequestException as e:
        app.logger.error(f"Analysis results service error: {e}")
        return None

def trigger_document_analysis_via_review_service(file_id, document_content):
    """Trigger analysis for a document using the review service"""
    try:
        # Convert document content to pages format expected by review service
        # Assuming the document content is text that needs to be split into pages
        pages = [document_content]  # Simple approach - treat entire content as one page
        
        # If document content is very long, you might want to split it
        # For now, keeping it simple
        
        # Prepare the review service request
        review_request = {
            "pages": pages,
            "file_id": file_id
        }
        
        app.logger.info(f"Calling review service for file_id: {file_id}")
        
        # Call review service
        resp = requests.post(
            f"{REVIEW_SERVICE_URL}/review-service",
            json=review_request,
            timeout=120
        )
        
        if resp.status_code == 200:
            review_result = resp.json()
            app.logger.info(f"Review service completed for file {file_id}")
            app.logger.info(f"Review result: {review_result}")
            return True
        else:
            app.logger.error(f"Review service error: {resp.status_code} - {resp.text}")
            return False
            
    except Exception as e:
        app.logger.error(f"Error triggering review service for file {file_id}: {e}")
        return False

def parse_document_content(document):
    """Parse document content from various formats"""
    document_content = ""
    
    if document.get('file'):
        file_data = document['file']
        
        # Handle string format (JSON string)
        if isinstance(file_data, str):
            try:
                file_data = json.loads(file_data)
            except json.JSONDecodeError:
                # If it's not JSON, treat as plain text
                document_content = file_data
                return document_content
        
        # Handle object format
        if isinstance(file_data, dict):
            # Check for OCR text
            if 'text' in file_data:
                document_content = file_data['text']
            # Check for other text fields
            elif 'content' in file_data:
                document_content = file_data['content']
            # Check for message field (might contain text)
            elif 'message' in file_data and file_data['message'] == 'OCR successful':
                # This might be a case where text is in a different structure
                document_content = str(file_data)
    
    return document_content

def validate_analysis_results(analysis_results):
    """Validate and ensure analysis results are in expected format"""
    if not analysis_results:
        return False
    
    if isinstance(analysis_results, list) and len(analysis_results) > 0:
        return True
    
    return False

@app.route('/history', methods=['GET', 'OPTIONS'])
def get_user_history():
    """Get all documents for the current user with their analysis results"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        documents = get_documents_by_user_uuid(user_uuid)
        
        enhanced_documents = []
        for doc in documents:
            file_id = doc.get('id')
            if not file_id:
                app.logger.warning(f"Document missing ID: {doc}")
                continue
                
            analysis_results = get_analysis_results(file_id)
            has_analysis = validate_analysis_results(analysis_results)
            
            enhanced_doc = {
                "document": doc,
                "analysis_results": analysis_results,
                "has_analysis": has_analysis
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
        app.logger.error(f"Unexpected error in get_user_history: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/history/analyze/<document_id>', methods=['POST', 'OPTIONS'])
def analyze_document(document_id):
    """Trigger analysis for a specific document via review service"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        # Get document details
        document = get_document_from_storage(document_id)
        
        # Check if document already has analysis
        existing_analysis = get_analysis_results(document_id)
        if validate_analysis_results(existing_analysis):
            return jsonify({
                "message": "Document already has analysis results",
                "has_analysis": True
            }), 200
        
        # Extract document content
        document_content = parse_document_content(document)
        
        if not document_content or document_content.strip() == "":
            return jsonify({"error": "No content found in document for analysis"}), 400
        
        app.logger.info(f"Document content length: {len(document_content)}")
        app.logger.info(f"Document content preview: {document_content[:200]}...")
        
        # Trigger analysis in background via review service
        def run_analysis():
            trigger_document_analysis_via_review_service(document_id, document_content)
        
        analysis_thread = threading.Thread(target=run_analysis)
        analysis_thread.daemon = True
        analysis_thread.start()
        
        return jsonify({
            "message": "Analysis started for document via review service",
            "document_id": document_id,
            "status": "processing"
        }), 202
        
    except requests.RequestException as e:
        if "404" in str(e):
            return jsonify({"error": "Document not found"}), 404
        return jsonify({"error": "Failed to analyze document", "details": str(e)}), 502
    except Exception as e:
        app.logger.error(f"Unexpected error in analyze_document: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/history/analyze-batch', methods=['POST', 'OPTIONS'])
def analyze_batch_documents():
    """Trigger analysis for multiple documents that don't have analysis via review service"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        # Get all user documents
        documents = get_documents_by_user_uuid(user_uuid)
        
        # Filter documents without analysis
        unanalyzed_docs = []
        for doc in documents:
            file_id = doc.get('id')
            if file_id:
                analysis_results = get_analysis_results(file_id)
                if not validate_analysis_results(analysis_results):
                    unanalyzed_docs.append(doc)
        
        if not unanalyzed_docs:
            return jsonify({
                "message": "All documents already have analysis results",
                "total_documents": len(documents),
                "unanalyzed_count": 0
            }), 200
        
        # Trigger analysis for unanalyzed documents
        def run_batch_analysis():
            for doc in unanalyzed_docs:
                file_id = doc.get('id')
                
                # Extract document content
                document_content = parse_document_content(doc)
                
                if document_content and document_content.strip():
                    app.logger.info(f"Processing document {file_id} in batch")
                    trigger_document_analysis_via_review_service(file_id, document_content)
                else:
                    app.logger.warning(f"Skipping document {file_id} - no content found")
        
        batch_thread = threading.Thread(target=run_batch_analysis)
        batch_thread.daemon = True
        batch_thread.start()
        
        return jsonify({
            "message": "Batch analysis started via review service",
            "total_documents": len(documents),
            "unanalyzed_count": len(unanalyzed_docs),
            "status": "processing"
        }), 202
        
    except Exception as e:
        app.logger.error(f"Unexpected error in analyze_batch_documents: {e}")
        return jsonify({"error": "Internal server error"}), 500

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
        has_analysis = validate_analysis_results(analysis_results)
        
        return jsonify({
            "document": document,
            "analysis_results": analysis_results,
            "has_analysis": has_analysis
        }), 200
        
    except requests.RequestException as e:
        if "404" in str(e):
            return jsonify({"error": "Document not found"}), 404
        return jsonify({"error": "Failed to retrieve document history", "details": str(e)}), 502
    except Exception as e:
        app.logger.error(f"Unexpected error in get_document_history: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/history/analysis/<document_id>', methods=['GET', 'OPTIONS'])
def get_document_analysis_only(document_id):
    """Get only the analysis results for a specific document"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        # Verify document exists (optional - remove if not needed)
        document = get_document_from_storage(document_id)
        analysis_results = get_analysis_results(document_id)
        
        if not validate_analysis_results(analysis_results):
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
        app.logger.error(f"Unexpected error in get_document_analysis_only: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/history/summary', methods=['GET', 'OPTIONS'])
def get_history_summary():
    """Get summary statistics of user's document history"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    user_uuid = get_current_user()
    if not user_uuid:
        return jsonify({"error": "Unable to identify user"}), 400

    try:
        documents = get_documents_by_user_uuid(user_uuid)
        
        total_documents = len(documents)
        documents_with_analysis = 0
        
        for doc in documents:
            file_id = doc.get('id')
            if not file_id:
                continue
                
            analysis_results = get_analysis_results(file_id)
            
            if validate_analysis_results(analysis_results):
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
        app.logger.error(f"Unexpected error in get_history_summary: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "history-service"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5030, debug=True)
