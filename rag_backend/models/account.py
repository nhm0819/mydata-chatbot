from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import Column, select, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from rag_backend.models import Base


class Account(Base):
    __tablename__ = "account"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(40), nullable=False, index=True, unique=True)
    create_at = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())

    def dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @staticmethod
    def from_schema(schema: BaseModel):
        fields = set(inspect(Account).attrs.keys())
        dictionary = {f: v for f, v in schema.dict().items() if f in fields}
        orm = Account(**dictionary)
        return orm

    def __repr__(self):
        return f"Account(id={self.id}, uid='{self.uid})'"
