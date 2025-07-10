"""
规划API路由

提供规划完成API端点，支持流式响应。
"""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Header

from src.api.chathistory.models.save_part import SaveChatHistoryRequest
from src.base.util.log_util import logger

router = APIRouter(prefix="/remote", tags=["remote"])


@router.post("/im_chat_history/save_part")
async def save_chat_history(request: SaveChatHistoryRequest, authorization: str = Header(None)) -> dict[str, Any]:
    """
    保存聊天历史API端点
curl 'http://localhost:5001/v1.0/invoke/planning-api/method/remote/im_chat_history/save_part' \
-X POST \
-H 'authorization: token c77eb8509f7d6bfa3db8af4d152e27dcb2b32c64' \
-H 'content-type: application/json' \
--data-raw '{"data":{"chat_name":"王和平, 李菊巨, Hilman obuy, KevinVasa","messages":[{"content":"Test","is_from_current_user":true,"timestamp":"3:07 PM","user_name":null},{"content":"Hi","is_from_current_user":false,"timestamp":"7:09 PM","user_name":"王和平"}]},"is_oldest_reached":false,"package_name":"jp.naver.line.android","session_id":"xxx","task_id":"111222","type":"AMChatHistoryMsg"}'
    """
    # 获取并记录 token
    token = None
    if authorization:
        # 处理 "token xxx" 格式的 authorization header
        if authorization.startswith("token "):
            token = authorization[6:]  # 去掉 "token " 前缀
        else:
            token = authorization

    # 记录请求信息
    logger.info("=== 保存聊天历史请求 ===")
    logger.info(f"Token: {token}")
    logger.info(f"Session ID: {request.session_id}")
    logger.info(f"Task ID: {request.task_id}")
    logger.info(f"Package Name: {request.package_name}")
    logger.info(f"Type: {request.type}")
    logger.info(f"Is Oldest Reached: {request.is_oldest_reached}")

    # 记录聊天数据
    logger.info(f"Chat Name: {request.data.chat_name}")
    logger.info(f"Messages Count: {len(request.data.messages)}")

    # 记录每条消息的详细信息
    for i, message in enumerate(request.data.messages):
        logger.info(f"Message {i + 1}:")
        logger.info(f"  Content: {message.content}")
        logger.info(f"  From Current User: {message.is_from_current_user}")
        logger.info(f"  Timestamp: {message.timestamp}")
        logger.info(f"  User Name: {message.user_name}")

    logger.info("=== 请求处理完成 ===")

    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "session_id": request.session_id,
        "task_id": request.task_id,
        "messages_count": len(request.data.messages),
    }
