from typing import Generic, Literal, Any, Optional

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Class for storing a piece of text and associated metadata."""

    page_content: str
    metadata: dict = Field(default_factory=dict)
    type: Literal["Document"] = "Document"


class DocumentBase(BaseModel):
    id: Optional[int]
    filename: str


class DocumentCreate(BaseModel):
    filename: str


class DocumentUpdate(BaseModel):
    id: int
    filename: str
