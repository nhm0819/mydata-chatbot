import logging

from fastapi import APIRouter
from starlette.responses import PlainTextResponse

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", response_class=PlainTextResponse)
async def index():
    """Index Page of the API."""
    return "Hello, World!"
