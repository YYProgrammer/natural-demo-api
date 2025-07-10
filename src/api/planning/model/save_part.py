"""Planning request models."""

from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """聊天消息模型"""

    content: str = Field(description="消息内容", example="Test", min_length=1)
    is_from_current_user: bool = Field(description="是否来自当前用户", example=True)
    timestamp: str = Field(description="消息时间戳", example="3:07 PM", min_length=1)
    user_name: Optional[str] = Field(default=None, description="用户名", example="王和平")


class ChatData(BaseModel):
    """聊天数据模型"""

    chat_name: str = Field(description="聊天名称/参与者", example="王和平, 李菊巨, Hilman obuy, KevinVasa", min_length=1)
    messages: List[ChatMessage] = Field(description="消息列表", min_items=1)


class SaveChatHistoryRequest(BaseModel):
    """保存聊天历史请求模型"""

    data: ChatData = Field(description="聊天数据")
    is_oldest_reached: bool = Field(description="是否已到达最早消息", example=False)
    package_name: str = Field(description="应用包名", example="jp.naver.line.android", min_length=1)
    session_id: str = Field(description="会话ID", example="xxx", min_length=1)
    task_id: str = Field(description="任务ID", example="111222", min_length=1)
    type: str = Field(description="消息类型", example="AMChatHistoryMsg", min_length=1)
