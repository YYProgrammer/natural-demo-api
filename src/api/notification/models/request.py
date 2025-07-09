"""Notification request models."""

from typing import Any, Dict

from pydantic import BaseModel, Field


class NotificationBody(BaseModel):
    """通知消息体"""

    type: str = Field(description="消息类型", example="notification", min_length=1, max_length=50)
    package_name: str | None = Field(default=None, description="包名称", example="com.example.app", max_length=100)
    data: Dict[str, Any] | None = Field(default=None, description="消息数据", example={"key": "value", "count": 42})


class Notification(BaseModel):
    """统一消息体"""

    # 元数据
    id: str | None = Field(default=None, description="消息唯一标识符", example="msg_123456789", max_length=100)
    name: str | None = Field(default=None, description="消息名称", example="系统通知", max_length=200)
    created: int | None = Field(default=None, description="创建时间戳（毫秒）", example=1640995200000, ge=0)
    arrival: int | None = Field(default=None, description="到达时间戳（毫秒）", example=1640995200000, ge=0)

    # 消息数据
    body: NotificationBody = Field(
        description="通知消息体",
        example=NotificationBody(
            type="notification", package_name="com.example.app", data={"title": "新消息", "content": "您有一条新消息"}
        ),
    )
