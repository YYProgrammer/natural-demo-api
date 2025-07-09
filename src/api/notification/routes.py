"""
通知API路由

提供通知发布API端点，支持多种消息类型处理。
"""

from datetime import datetime

from fastapi import APIRouter, Header, HTTPException

from src.api.notification.models.request import Notification
from src.services.notification.notification_service import notification_service

router = APIRouter(prefix="/notification", tags=["notification"])


@router.post("/publish")
async def publish_notification(
    notification: Notification, authorization: str = Header(..., description="Authorization token")
):
    """
    发布通知

    接收统一格式的消息体，处理不同类型的通知消息。

    Args:
        notification: 通知消息体
        authorization: Authorization header中的token

    Returns:
        dict: 处理结果，包含状态和消息ID
    """
    try:
        # 提取token
        if authorization.startswith("token "):
            token = authorization[6:]  # 移除 "token " 前缀
        else:
            token = authorization

        # notification_service = NotificationService()

        # 调用通知处理服务
        result = await notification_service.process_message(notification, token)

        if result["success"]:
            return {
                "status": "success",
                "notification_id": result["message_id"],
                "token": token,
                "timestamp": datetime.now().isoformat(),
            }
        else:
            raise HTTPException(status_code=500, detail=f"通知处理失败: {result['error']}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"通知处理失败: {str(e)}")
