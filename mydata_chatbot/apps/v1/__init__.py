import sys

try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

from http.client import HTTPException
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.staticfiles import StaticFiles

from mydata_chatbot import apis
from mydata_chatbot.assemble import event
from mydata_chatbot.assemble import exception
from mydata_chatbot.assemble.middleware import cors_middleware

app = FastAPI(
    docs_url="/docs",
    middleware=[
        cors_middleware,
    ],
)

# add static files
current_path = Path(__file__).resolve().parent
static_path = current_path.parent.parent.joinpath("static")
static_files = StaticFiles(directory=static_path)
app.mount("/static", static_files, name="static")

# add events
app.add_event_handler("startup", event.startup_event_1)
app.add_event_handler("startup", event.startup_event_2)
app.add_event_handler("shutdown", event.shutdown_event)

# add exception handlers
app.add_exception_handler(Exception, exception.exception_handler)
app.add_exception_handler(HTTPException, exception.http_exception_handler)
app.add_exception_handler(
    RequestValidationError, exception.validation_exception_handler
)

# add routers
app.include_router(apis.v1.index.router)
app.include_router(apis.v1.chat.router)
app.include_router(apis.v1.data.router)
