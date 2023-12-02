# data.py

from fastapi import HTTPException
from fastapi.responses import (
    RedirectResponse, Response, FileResponse,
    JSONResponse, HTMLResponse, StreamingResponse,
    PlainTextResponse, UJSONResponse, ORJSONResponse
)

__all__ = [
    "GET",
    "POST",
    "DELETE",
    "UPLOAD",
    "HEAD",
    "PATCH",
    "PUT",
    "DOCS",
    "FAVICON",
    "METHODS",
    "RedirectResponse",
    "Response",
    "FileResponse",
    "JSONResponse",
    "HTMLResponse",
    "StreamingResponse",
    "PlainTextResponse",
    "UJSONResponse",
    "ORJSONResponse",
    "RESPONSES",
    "HTTPException"
]

DOCS = '/docs'
FAVICON = '/favicon.ico'

class Methods:
    """A class to contain the methods of the service."""

    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    UPLOAD = "UPLOAD"
    HEAD = "HEAD"
    PATCH = "PATCH"
    PUT = "PUT"

    METHODS = (
        GET, POST, DELETE, UPLOAD,
        HEAD, PATCH, PUT
    )
# end Methods

GET = Methods.GET
POST = Methods.POST
DELETE = Methods.DELETE
UPLOAD = Methods.UPLOAD
HEAD = Methods.HEAD
PATCH = Methods.PATCH
PUT = Methods.PUT

METHODS = Methods.METHODS

RESPONSES = (
    RedirectResponse, Response,
    FileResponse, JSONResponse,
    HTMLResponse, StreamingResponse,
    PlainTextResponse, UJSONResponse,
    ORJSONResponse
)