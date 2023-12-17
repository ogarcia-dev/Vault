from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped, 
    mapped_column
)

from . import Base



class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())