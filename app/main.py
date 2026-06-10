import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.core.errors import OpenClawAdapterError
from app.core.logging import setup_logging
from app.routers import deals, health

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Hub OpenClaw Adapter")

app.include_router(health.router)
app.include_router(deals.router, prefix="/deals")


@app.exception_handler(OpenClawAdapterError)
async def openclaw_adapter_error_handler(
    _request: Request,
    exc: OpenClawAdapterError,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "ok": False,
            "error": exc.error,
            "message": exc.message,
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse(
            status_code=401,
            content={"detail": exc.detail},
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception):
    logger.exception("Unhandled error: %s", type(exc).__name__)
    return JSONResponse(
        status_code=500,
        content={
            "ok": False,
            "error": "internal_error",
            "message": "Internal server error",
        },
    )
