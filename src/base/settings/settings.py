"""
API配置模块

包含API服务、路由、中间件等相关的配置设置。
"""

from pydantic import BaseModel

from src.util.os_util import get_env


class Settings(BaseModel):
    """API配置类"""

    # API基本配置
    api_port: int = 11915
    api_prefix: str = get_env("API_PREFIX", "/v1.0/invoke/planning-api/method")
    api_apidoc_token: str = get_env("API_APIDOC_TOKEN", "33LpV41dWu5PXfaj")


settings = Settings()
