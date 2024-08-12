"""NOT IMPLEMENTED."""

from fastapi import FastAPI
from starlette.responses import PlainTextResponse

from rag_backend.assemble.middleware import cors_middleware

app = FastAPI(
    docs_url="/docs",
    middleware=[
        cors_middleware,
    ],
)


@app.get("/", response_class=PlainTextResponse)
async def index():
    """Index Page of the API."""
    return "Hello, World!"
