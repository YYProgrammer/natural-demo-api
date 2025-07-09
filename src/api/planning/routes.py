"""
规划API路由

提供规划完成API端点，支持流式响应。
"""

import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter(prefix="/v1.0/invoke/planning-api/method/ai_phone/planning", tags=["planning"])


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
        data_file = os.path.join(current_dir, 'data', 'response_1.json')
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

    Args:
        request: 包含 session_id, stream, query 的请求体

    Returns:
        流式JSON数据
    """
    return StreamingResponse(stream_generator(request.session_id, request.query), media_type="text/plain")
