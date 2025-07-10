"""API configuration for managing routes."""

from fastapi import APIRouter, FastAPI

from src.api.chathistory.routes import router as router_chathistory
from src.api.hello.routes import router as router_hello
from src.api.notification.routes import router as router_notification
from src.api.planning.routes import router as router_planning


class ApiConfig:
    """API configuration class for managing route registration."""

    _router_list: list[APIRouter]

    def __init__(self) -> None:
        """Initialize API configuration with router list."""
        # 应用配置
        self._router_list = [
            router_hello,  # 健康检查路由
            router_planning,  # 规划API路由
            router_notification,  # 通知API路由
            router_chathistory,  # 聊天历史API路由
        ]

    def apply(self, app: FastAPI, api_prefix: str) -> None:
        """Apply all routers to the FastAPI app.

        Args:
            app: FastAPI application instance
            api_prefix: API prefix for all routes
        """
        for router in self._router_list:
            app.include_router(router=router, prefix=api_prefix)


# 创建全局实例
api_config = ApiConfig()
