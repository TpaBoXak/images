from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
import base64
import hashlib


from config import settings
from app import db_helper
from app.dao import images as image_dao
from app.utils.check_users import get_current_user
from app.schemas.images import ImageSchema
from app.schemas.images import ImageTitle


router: APIRouter = APIRouter(prefix=settings.api.images_prefix)

@router.get("/all", response_model=list[ImageSchema])
async def get_all_images(
    session: AsyncSession = Depends(db_helper.session_getter),
    user_id: int = Depends(get_current_user)
):
    images_data: list[ImageSchema] = await image_dao.get_iamges(session=session)

    return images_data


@router.post("/add", response_model=ImageSchema)
async def add_image(
    session: AsyncSession = Depends(db_helper.session_getter),
    user_id: int = Depends(get_current_user),
    file: UploadFile = File(...)
):
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension. Only png, jpg, and jpeg are allowed."
        )
    
    str_for_hash = file.filename + datetime.today().isoformat()
    file_hash = hashlib.md5(str_for_hash.encode()).hexdigest()
    hashed_filename = f"{file_hash}.{file_extension}"
    
    image_schema: Optional[ImageSchema] = await image_dao.add_image(
        session=session,
        file=file,
        hashed_filename=hashed_filename
    )

    if not image_schema:
        raise HTTPException(status_code=500, detail="File not save")
    
    content_base64 = base64.b64encode(await file.read()).decode('utf-8')
    payload = {
        "filename": hashed_filename,
        "content": content_base64
    }
    await image_dao.send_image_task(type="upload", payload=payload)
        
    return image_schema

@router.post("/update")
async def add_image(
    update_file: ImageTitle,
    session: AsyncSession = Depends(db_helper.session_getter),
    user_id: int = Depends(get_current_user),
):
    if await image_dao.update_image(session=session, update_info=update_file):
        return {"message": "Image update successfully"}
    raise HTTPException(status_code=500, detail="Image not update")

@router.delete("/delete/{image_id}")
async def add_image(
    image_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user_id: int = Depends(get_current_user),
):
    image_path = await image_dao.delete_image(session=session, image_id=image_id)
    
    if image_path:
        payload = {
            "path": image_path,
        }
        await image_dao.send_image_task(type="delete", payload=payload)
        return {"message": "Image deleted successfully"}
        
    raise HTTPException(status_code=500, detail="Image not delete")