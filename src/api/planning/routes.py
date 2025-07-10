"""
规划API路由

提供规划完成API端点，支持流式响应。
"""

import asyncio
from datetime import datetime
import json
from typing import Any

from fastapi import APIRouter, Header, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.api.planning.models.request import SaveChatHistoryRequest
from src.base.util.log_util import logger

router = APIRouter(prefix="/ai_phone/planning", tags=["planning"])


class PlanningRequest(BaseModel):
    """规划请求模型"""

    session_id: str
    stream: bool = True
    query: str = ""


def generate_stream(session_id: str, query: str) -> str:
    """生成流式响应数据"""
    # 读取 src/api/planning/data/response_1.json 文件
    try:
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(current_dir, "data", "response_1.json")
        with open(data_file, "r", encoding="utf-8") as f:
            response = json.load(f)

        # 更新 session_id 和 focus 字段
        if session_id:
            response["session_id"] = session_id
        if query and "screens" in response and len(response["screens"]) > 0:
            response["screens"][0]["focus"] = query

    except FileNotFoundError:
        # 如果文件不存在，使用默认响应
        response = {
            "session_id": session_id,
            "screens": [
                {
                    "name": "main",
                    "key": "e77b28b0c42672dba773d7564f6dda4a",
                    "state": "active",
                    "title": "Group Travel Planning",
                    "description": "Main screen for collaborative travel planning and coordination.",
                    "icon": "",
                    "focus": query,
                    "interaction_value": "",
                    "interaction_template": "",
                    "cards": [],
                }
            ],
        }
    except json.JSONDecodeError:
        # 如果 JSON 解析失败，使用默认响应
        response = {"session_id": session_id, "error": "JSON decode error in response file"}

    return f"data: {json.dumps(response)}\n\n"


async def stream_generator(session_id: str, query: str):
    """异步流式生成器"""
    # 发送初始响应
    yield generate_stream(session_id, query)
    await asyncio.sleep(0.1)

    # 重复发送相同的响应（模拟最后几次相同的数据）
    for _ in range(2):
        yield generate_stream(session_id, query)
        await asyncio.sleep(0.1)


@router.post("/completions")
async def planning_completions(request: PlanningRequest) -> StreamingResponse:
    """
    规划完成API端点 - 流式响应

    curl -X POST "http://localhost:5001/planning-api/api/ai_phone/planning/completions" \
      -H "Content-Type: application/json" \
      -d '{
        "session_id": "bb32bf31-7892-4069-ba6b-96ca4b80e886",
        "stream": true,
        "query": "hi"
      }'


    Args:
        request: 包含 session_id, stream, query 的请求体

    Returns:
        流式JSON数据
    """
    return StreamingResponse(stream_generator(request.session_id, request.query), media_type="text/plain")


@router.post("/im_chat_history/save_part")
async def save_chat_history(
    request: SaveChatHistoryRequest,
    authorization: str = Header(None)
) -> dict[str, Any]:
    """
    保存聊天历史API端点

    curl 'http://localhost:5001/planning-api/api/ai_phone/planning/im_chat_history/save_part' \
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
        logger.info(f"Message {i+1}:")
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
        "messages_count": len(request.data.messages)
    }