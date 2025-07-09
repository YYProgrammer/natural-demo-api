"""
API配置模块

包含API服务、路由、中间件等相关的配置设置。
"""

from pydantic import BaseModel


class Settings(BaseModel):
    """API配置类"""

    # API基本配置
    api_port: int = 5001
    api_prefix: str = "/v1.0/invoke/planning-api/method"


settings = Settings()
