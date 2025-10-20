"""
Error handlers for the API.

This module defines error handlers for various exceptions that can be raised
during API request processing.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    GateDetectorException,
    CameraConnectionError,
    FrameCaptureError,
    GateDetectionError
)


# pylint: disable=unused-argument
async def gate_detector_exception_handler(
    request: Request, exc: GateDetectorException
) -> JSONResponse:
    """
    Handle GateDetectorException and its subclasses.

    Args:
        request: The request that caused the exception.
        exc: The exception that was raised.

    Returns:
        A JSON response with the error details.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": None, "message": exc.message},
    )


async def camera_connection_error_handler(
    request: Request, exc: CameraConnectionError
) -> JSONResponse:
    """
    Handle CameraConnectionError.

    Args:
        request: The request that caused the exception.
        exc: The exception that was raised.

    Returns:
        A JSON response with the error details.
    """
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": None, "message": exc.message},
    )


async def frame_capture_error_handler(
    request: Request, exc: FrameCaptureError
) -> JSONResponse:
    """
    Handle FrameCaptureError.

    Args:
        request: The request that caused the exception.
        exc: The exception that was raised.

    Returns:
        A JSON response with the error details.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": None, "message": exc.message},
    )


async def gate_detection_error_handler(
    request: Request, exc: GateDetectionError
) -> JSONResponse:
    """
    Handle GateDetectionError.

    Args:
        request: The request that caused the exception.
        exc: The exception that was raised.

    Returns:
        A JSON response with the error details.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": None, "message": exc.message},
    )


def register_exception_handlers(app):
    """
    Register exception handlers with the FastAPI application.

    Args:
        app: The FastAPI application.
    """
    app.add_exception_handler(GateDetectorException, gate_detector_exception_handler)
    app.add_exception_handler(CameraConnectionError, camera_connection_error_handler)
    app.add_exception_handler(FrameCaptureError, frame_capture_error_handler)
    app.add_exception_handler(GateDetectionError, gate_detection_error_handler)
