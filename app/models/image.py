from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import func

from datetime import datetime

from .base import Base

class Image(Base):
    __tablename__ = "images"
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    path: Mapped[str] = mapped_column(String(256), nullable=False)
    resolution: Mapped[str] = mapped_column(String(128), nullable=False)
    size: Mapped[float] = mapped_column(Float, nullable=False)
    time_created: Mapped[datetime] = mapped_column(DateTime, nullable=False,
            server_default=func.now())
