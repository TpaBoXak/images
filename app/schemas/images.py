from pydantic import BaseModel

class ImageSchema(BaseModel):
    id: int
    file: str
    title: str

class ImageTitle(BaseModel):
    id: int
    new_title: str