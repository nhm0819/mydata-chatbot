from pydantic import BaseModel, field_validator

class ChatResponse(BaseModel):
    """Chat response schema"""

    sender: str
    message: str
    type: str
    xtra: dict = None

    @field_validator("sender")
    def sender_must_be_bot_or_you(cls, v):
        if v not in ["bot", "you"]:
            raise ValueError("sender must be bot or you")
        return v

    @field_validator("type")
    def validate_message_type(cls, v):
        if v not in ["start", "stream", "end", "error", "info"]:
            raise ValueError("type must be start, stream or end")
        return v
