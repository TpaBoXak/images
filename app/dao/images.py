from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
from fastapi import HTTPException
from fastapi import UploadFile
from typing import Optional
from aio_pika import connect_robust
from aio_pika import Message
import json

from config import settings
from app.models.image import Image
from app.schemas.images import ImageSchema
from app.schemas.images import ImageTitle


async def get_iamges(session: AsyncSession) -> list[ImageSchema]:
    stmt = select(Image)
    result = await session.execute(stmt)
    images: list[Image] = result.scalars()
    print(images)
    image_list = []
    for img in images:
        print(img)
        file_path = Path(settings.images_folder.path) / img.path
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        image_url = f"/static/{img.path}"
        image_list.append(ImageSchema(id=img.id, file=image_url, title=img.title))
    
    return image_list

async def send_image_task(type: str, payload: dict):
    connection = await connect_robust(settings.rabbitmq.url)
    async with connection:
        channel = await connection.channel()
        
        queue = await channel.declare_queue("image_tasks", durable=True)
        
        task_data = {
            "type": type,
            "payload": payload,
        }
        
        message = Message(body=json.dumps(task_data).encode())
        await channel.default_exchange.publish(
            message, routing_key=queue.name
        )


async def add_image(session: AsyncSession, file: UploadFile, hashed_filename: str) -> Optional[ImageSchema]:
    try:
        original_title = file.filename
        file_size_kb = len(await file.read()) / 1024
        file.file.seek(0)

        new_image = Image(
            title=file.filename,
            path=hashed_filename,
            resolution="500x500",
            size=file_size_kb
        )
        session.add(new_image)
        await session.commit()
        await session.refresh(new_image)

        image_url = f"/static/{hashed_filename}"
    except:
        await session.rollback()
        return None
    else:
        session.commit()
        return ImageSchema(id=new_image.id, file=image_url, title=original_title)
    
async def update_image(session: AsyncSession, update_info: ImageTitle) -> bool:
    try:
        stmt = select(Image).where(Image.id == update_info.id)
        result = await session.execute(stmt)
        image: Image = result.scalar()
        if image is None:
            raise HTTPException(status_code=404, detail="Image not found")
        image.title = update_info.new_title
        session.add(image)
    except:
        await session.rollback()
        return False
    else:
        await session.commit()
        return True
    
async def delete_image(session: AsyncSession, image_id: int) -> Optional[str]:
    try:
        stmt = select(Image).where(Image.id == image_id)
        result = await session.execute(stmt)
        image: Image = result.scalar()
        if image is None:
            raise HTTPException(status_code=404, detail="Image not found")
        image_path = image.path
        await session.delete(image)
    except:
        await session.rollback()
        return None
    else:
        await session.commit()
        return image_path