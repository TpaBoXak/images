from fastapi import UploadFile
from fastapi import HTTPException

from config import settings

def validate_file_extension(file: UploadFile):
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file extension. Only png, jpg, and jpeg are allowed.")