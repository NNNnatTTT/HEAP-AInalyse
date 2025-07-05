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


def get_analsis_results():
    get_analsis_results_URL = f"http://localhost:<port>/get_results"
    try:
        response = requests.post(get_analsis_results_URL)
        if response.status_code == 200:
            data = response.json()
            results = data["results"]
            # Review pipelining
            
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return results



@app.route('/suggest', methods=['POST'])
def get_suggestions():
    # results = get_analsis_results()
    # Based on results, generate changes to rectify the issues

    get_analsis_results_URL = f"http://localhost:<port>/get_results"
    try:
        response = requests.post(get_analsis_results_URL)
        if response.status_code == 200:
            data = response.json()
            results = data["results"]
            # Review pipelining





            
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        return jsonify({"error": str(e)}), 500








# Evoke review when successful upload
# Review has a POST api called here
def review_doc(document_name):
    # Some POST api
    RS_review_url = f"http://<DSS_HOST>:<port>/review_document/<{document_name}>"
    try:
        response = requests.post(RS_review_url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/upload-service', methods=['POST'])
def upload_document():
    # Call document-storage-service upload
    # Pass document into this service review_doc()
    # review_doc() calls review service to continue
    DSS_upload_url = f"http://<DSS_HOST>:<port>/upload_document"

    try:
        response = requests.post(DSS_upload_url)
        if response.status_code == 200:
            data = response.json()
            document = data["stored_filename"]
            # Review pipelining
            review_doc(document) # Is string ig
            
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
    
# This for dashboard actually, unless want to show recent docs list
# @app.route('/upload-service/get-all', methods=['GET'])
# def get_all_documents():

# @app.route('/upload-service/<document_id>', methods=['GET'])
# def get_document(document_id):

# def delete_document(document_id):

# def update_document(document_id):


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9697,debug=True)