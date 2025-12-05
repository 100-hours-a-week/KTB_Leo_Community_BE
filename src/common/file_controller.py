from fastapi import APIRouter, UploadFile, File, Depends
from common.file_service import FileService

router = APIRouter(prefix="/upload", tags=["files"])

def get_file_service():
    return FileService()

@router.post("", response_model=str)
def upload_file(
    file: UploadFile = File(...),
    service: FileService = Depends(get_file_service)
):
    return service.upload_image(file)