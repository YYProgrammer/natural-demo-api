"""Notification request models."""

from typing import Any, Dict

from pydantic import BaseModel, Field


class NotificationBody(BaseModel):
    """通知消息体"""

    type: str = Field(description="消息类型", min_length=1, max_length=50)
    package_name: str | None = Field(default=None, description="包名称", max_length=100)
    session_id: str | None = Field(default=None, description="会话ID", max_length=100)
    task_id: str | None = Field(default=None, description="任务ID", max_length=100)
    data: Dict[str, Any] | None = Field(default=None, description="消息数据")


class Notification(BaseModel):
    """统一消息体"""

    # 元数据
    id: str | None = Field(default=None, description="消息唯一标识符", max_length=100)
    name: str | None = Field(default=None, description="消息名称", max_length=200)
    created: int | None = Field(default=None, description="创建时间戳（毫秒）", ge=0)
    arrival: int | None = Field(default=None, description="到达时间戳（毫秒）", ge=0)

    # 消息数据
    body: NotificationBody = Field(
        description="通知消息体",
    )
