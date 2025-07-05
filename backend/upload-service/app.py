from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": ["http://localhost:5173"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}})

# Example service URLs (replace with your actual endpoints)
SCANNER_URL = "SCANNER_URL"
DOCUMENT_SERVICE = "DOCUMENT_URL"
AI_SERVICE = "AI_URL"

@app.route('/upload-service', methods=['POST'])
def upload_and_process_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    try:
        # 1. Send PDF to scanner service
        scanner_response = requests.post(
            SCANNER_URL,
            files={'file': (file.filename, file, 'application/pdf')}
        )
        if scanner_response.status_code != 200:
            return jsonify({"error": "Scanner service error", "details": scanner_response.text}), 500

        scanner_json = scanner_response.json()

        # 2. Send scanner output to second service
        second_response = requests.post(
            DOCUMENT_SERVICE,
            json=scanner_json
        )
        if second_response.status_code != 200:
            return jsonify({"error": "Second service error", "details": second_response.text}), 500

        second_json = second_response.json()

        # 3. Send second service output to third service
        third_response = requests.post(
            AI_SERVICE,
            json=second_json
        )
        if third_response.status_code != 200:
            return jsonify({"error": "Third service error", "details": third_response.text}), 500

        final_json = third_response.json()
        return jsonify(final_json), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9697, debug=True)
