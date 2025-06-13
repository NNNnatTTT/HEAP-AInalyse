# In service/document_service.py
from repository.document_repository import upload_document, get_document_url, delete_document
from fastapi import UploadFile

def handle_upload(user_id: str, file: UploadFile):
    return upload_document(user_id, file)

def handle_download(path: str):
    return get_document_url(path)

def handle_delete(path: str):
    return delete_document(path)
