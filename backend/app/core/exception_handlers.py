"""Centralized FastAPI exception handlers."""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


logger = logging.getLogger(__name__)


def register_exception_handlers(application: FastAPI) -> None:
    """Register shared exception handlers on the FastAPI application."""
    application.add_exception_handler(StarletteHTTPException, handle_http_exception)
    application.add_exception_handler(RequestValidationError, handle_validation_error)
    application.add_exception_handler(Exception, handle_unexpected_error)


async def handle_http_exception(
    request: Request,
    exception: StarletteHTTPException,
) -> JSONResponse:
    """Return documented JSON for HTTP errors."""
    del request
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "success": False,
            "message": str(exception.detail),
            "errors": [],
        },
    )


async def handle_validation_error(
    request: Request,
    exception: RequestValidationError,
) -> JSONResponse:
    """Return documented JSON for request-validation errors."""
    del request
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed.",
            "errors": [_format_validation_error(error) for error in exception.errors()],
        },
    )


async def handle_unexpected_error(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    """Log unexpected errors without exposing internal details."""
    logger.exception("Unhandled request error for %s", request.url.path, exc_info=exception)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error.",
            "errors": [],
        },
    )


def _format_validation_error(error: dict[str, Any]) -> dict[str, str]:
    """Map FastAPI validation metadata to the documented error format."""
    location = error.get("loc", ())
    field = ".".join(str(part) for part in location if part != "body")
    return {"field": field, "message": error["msg"]}
