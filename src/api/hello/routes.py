"""
健康检查API路由

提供系统健康状态检查，包括数据库连接池状态监控。
"""

from typing import Any

from fastapi import APIRouter

router = APIRouter(tags=["hello"])


@router.get("/")
async def check() -> dict[str, str]:
    """基础健康检查."""
    return {"status": "success", "message": "服务运行正常"}


@router.get("/{name}")
async def hello(name: str) -> dict[str, Any]:
    return {
        "message": f"Hello, {name}",
    }
