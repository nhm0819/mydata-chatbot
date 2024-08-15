from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import Column, select, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from rag_backend.models import Base


class Document(Base):
    __tablename__ = "document"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename = mapped_column(String(200), unique=True, nullable=False)
    create_at = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
