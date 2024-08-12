from typing import Generic, Literal, Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Class for storing a piece of text and associated metadata."""

    page_content: str
    metadata: dict = Field(default_factory=dict)
    type: Literal["Document"] = "Document"
