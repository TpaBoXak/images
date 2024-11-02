from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy import DateTime
from sqlalchemy import func

from datetime import datetime

from .base import Base

class User(Base):
    __tablename__ = "users"
    first_name: Mapped[str] = mapped_column(String(32), nullable=False)
    second_name: Mapped[str] = mapped_column(String(32), nullable=False)
    nickname: Mapped[str] = mapped_column(String(32), unique=True,
            nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255),
            nullable=False)
    time_created: Mapped[datetime] = mapped_column(DateTime, nullable=False,
            server_default=func.now())
    