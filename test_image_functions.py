import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from app.dao.images import add_image, update_image, delete_image
from app.schemas.images import ImageSchema, ImageTitle
from app.models.image import Image

@pytest.mark.asyncio
async def test_add_image_success():
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_image.jpg"
    mock_file.read = AsyncMock(return_value=b"some file content")
    mock_file.file = MagicMock()
    mock_file.file.seek = MagicMock()

    mock_session = AsyncMock(spec=AsyncSession)

    mock_image = MagicMock(spec=Image)
    mock_image.id = 1
    mock_image.path = "hashed_test_image.jpg"
    mock_image.title = "test_image.jpg"
    mock_image.resolution = "500x500"
    mock_image.size = 0.024

    mock_session.commit = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.add = MagicMock()

    with patch("app.dao.images.Image", return_value=mock_image):
        result = await add_image(mock_session, mock_file, "hashed_test_image.jpg")

    assert result == ImageSchema(id=1, file="/static/hashed_test_image.jpg", title="test_image.jpg")


@pytest.mark.asyncio
async def test_update_image_success():
    update_info = ImageTitle(id=1, new_title="new_title")
    
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.rollback = AsyncMock()
    
    mock_image = MagicMock(spec=Image)
    mock_image.id = 1
    mock_image.title = "old_title"
    
    mock_session.execute = AsyncMock(return_value=AsyncMock(scalar=MagicMock(return_value=mock_image)))

    with patch("app.dao.images.Image", new=Image):
        result = await update_image(mock_session, update_info)

    assert result is True
    assert mock_image.title == "new_title"


@pytest.mark.asyncio
async def test_delete_image_success():
    mock_session = AsyncMock(spec=AsyncSession)

    mock_image = MagicMock(spec=Image)
    mock_image.path = "test_image_path.jpg"
    mock_session.execute = AsyncMock(return_value=AsyncMock(scalar=MagicMock(return_value=mock_image)))


    mock_session.commit = AsyncMock()

    result = await delete_image(mock_session, image_id=1)

    assert result == "test_image_path.jpg"
