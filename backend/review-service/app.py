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

@app.route('/review_document/<document_id>', methods=['POST'])
def review_doc(document_name):
    # Get text for review
    # review based on training from correct contracts
    # Discrepencies are highlighted and the location
        # Of the fucked up lines are saved in JSON in analysis results
        # To be used by suggestions



    # From document-storage-service, NOT upload service
    DSS_getDocByID_url = f"http://localhost:<port>/get_document/{document_name}"

    try:
        response = requests.get(DSS_getDocByID_url)
        if response.status_code == 200:
            data = response.json()
            document = data["document"]
            # Review pipelining

        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9697,debug=True)