from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from pdf2image import convert_from_bytes
from PIL import Image 
import pytesseract    
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

@app.route('/add_session/<modsecyear>', methods=['GET'])
def add_session(modsecyear):
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


        # Check if data exists and return the first element, else return an error
        data = response.data
        if response:
            return jsonify(data), 200
        else:
            return jsonify({"error": "No matching modsecyear found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/scan_document', methods=['POST'])
def scan_document():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        filename = file.filename.lower()
        extracted_text = ""

        if filename.endswith('.pdf'):
            # Convert PDF pages to images
            images = convert_from_bytes(file.read())
            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image)
                extracted_text += f"\n--- Page {i+1} ---\n{text}"
        else:
            # Assume it's an image
            image = Image.open(file.stream)
            extracted_text = pytesseract.image_to_string(image)
        
        print(f"Extracted text: {extracted_text}")

        return jsonify({"message": "OCR successful", "text": extracted_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9697,debug=True)