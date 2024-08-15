import uuid
from pydantic import BaseModel, Field


class Prompt(BaseModel):
    user_query: str
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
