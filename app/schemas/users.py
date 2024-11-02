from pydantic import BaseModel
from typing import List, Optional

class UserBaseSchema(BaseModel):
    password: str
    nickname: str