from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from src.util.meta import Meta


def configure_exception_handlers(app):
    """配置异常处理"""
    app.add_exception_handler(Meta, meta_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)


async def meta_exception_handler(request: Request, exc: Meta):
    """处理 Meta 异常"""
    return JSONResponse(
        status_code=400,
        content={"name": exc.name, "message": exc.message, "data": exc.data},
    )


async def general_exception_handler(request: Request, exc: Exception):
    """处理通用异常"""
    return JSONResponse(
        status_code=500,
        content={"name": "internal_error", "message": str(exc), "data": None},
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """处理http异常"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"name": "http_error", "message": str(exc.detail), "data": None},
    )
