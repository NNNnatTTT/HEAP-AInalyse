from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from pdf2image import convert_from_bytes
from PIL import Image 
import pytesseract    
import os
import requests

app = Flask(__name__)
CORS(app)
# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



    
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
    app.run(host='0.0.0.0', port=5004,debug=True)