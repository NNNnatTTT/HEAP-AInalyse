#pip install flask pypdf python-dotenv

from flask import Blueprint, request, jsonify
from pypdf import PdfReader

scanner_bp = Blueprint('scanner', __name__)

@scanner_bp.route('/scan_document', methods=['POST'])
def scan_document():
    # 1) ensure file present
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    f = request.files['file']

    # 2) extract text
    reader = PdfReader(f.stream)
    pages = [page.extract_text() or "" for page in reader.pages]

    # 3) respond with JSON
    return jsonify({ "pages": pages })
