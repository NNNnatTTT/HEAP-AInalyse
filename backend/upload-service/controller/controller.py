from fastapi import APIRouter, UploadFile, File, HTTPException
from service.document_service import handle_upload, handle_download, handle_delete

router = APIRouter()

@router.post("/upload/")
async def upload(user_id: str, file: UploadFile = File(...)):
    result = handle_upload(user_id, file)
    if result is None:
        raise HTTPException(status_code=500, detail="Upload failed")
    return {"path": result}

@router.get("/download/")
async def download(path: str):
    url = handle_download(path)
    if not url:
        raise HTTPException(status_code=404, detail="File not found")
    return {"url": url}

@router.delete("/delete/")
async def delete(path: str):
    success = handle_delete(path)
    if not success:
        raise HTTPException(status_code=500, detail="Delete failed")
    return {"status": "deleted"}
