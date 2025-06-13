# from supabase import create_client, Client
# import os

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# def get_match_history():
#     response = supabase.table("match_history").select("*").execute()
#     return response.data

import os
from supabase import create_client, Client
from typing import Optional
from fastapi import UploadFile
import uuid

# Setup Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "documents"

# Upload a document
def upload_document(user_id: str, file: UploadFile) -> Optional[str]:
    # Generate a unique filename to avoid collisions
    file_ext = file.filename.split('.')[-1]
    unique_filename = f"{user_id}/{uuid.uuid4()}.{file_ext}"

    # Read file content
    content = file.file.read()

    # Upload to Supabase Storage
    result = supabase.storage.from_(BUCKET_NAME).upload(unique_filename, content)
    
    if result.get("error"):
        print("Upload error:", result["error"])
        return None

    return unique_filename

# Download a document (returns a public URL)
def get_document_url(path: str) -> Optional[str]:
    url = supabase.storage.from_(BUCKET_NAME).get_public_url(path)
    return url

# Delete a document
def delete_document(path: str) -> bool:
    result = supabase.storage.from_(BUCKET_NAME).remove([path])
    return not result.get("error")
