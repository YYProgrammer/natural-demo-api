"""
规划API路由

提供规划完成API端点，支持流式响应。
"""

import asyncio
import json
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Header, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from src.api.planning.model.planning_flow_type import PlanningTypeEnum
from src.api.planning.model.planning_interaction import PlanningInteraction
from src.api.planning.model.save_part import SaveChatHistoryRequest
from src.base.util.log_util import logger
from src.store.chat.chat_store import chat_store
from src.store.chat.chat_name_store import chat_name_store

router = APIRouter(prefix="/ai_phone/planning", tags=["planning"])


class PlanningRequest(BaseModel):
    """规划请求模型"""

    session_id: str
    stream: bool = True
    query: str = ""
    interactions: list[PlanningInteraction] = []


class PlanningSuggestionsRequest(BaseModel):
    """规划建议请求模型"""

    original_description: str


class PlanningChatRequest(BaseModel):
    """规划聊天请求模型"""

    session_id: str
    stream: bool = True
    query: str = ""


def generate_stream(session_id: str, query: str, response_file: str) -> str:
    """生成流式响应数据"""
    # 读取 src/api/planning/data/response_1.json 文件
    try:
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(current_dir, "data", response_file)
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


async def stream_generator(session_id: str, query: str, response_file: str):
    """异步流式生成器"""
    # 发送初始响应
    yield generate_stream(session_id, query, response_file)
    await asyncio.sleep(0.1)

    # 重复发送相同的响应（模拟最后几次相同的数据）
    for _ in range(2):
        yield generate_stream(session_id, query, response_file)
        await asyncio.sleep(0.1)


def response_by_interactions(interactions: list[PlanningInteraction]) -> str:
    if len(interactions) == 0:
        return "a2b_step_1.json"
    else:
        interaction = interactions[0]
        if interaction.type == "onCalendar":
            return "a2b_step_2.json"
        elif interaction.type == "onAccessPermissionReject":
            return "a2b_step_1.json"
        elif interaction.type == "onAccessPermissionConfirm":
            return "a2b_step_3.json"
        elif interaction.type == "onViewRoute":
            return "a2b_step_4.json"
        else:
            return "a2b_step_1.json"


@router.post("/suggestions")
async def planning_suggestions(request: PlanningSuggestionsRequest) -> JSONResponse:
    """
    规划建议API端点

    Args:
        request: 包含 original_description 的请求体

    Returns:
        JSON数据
    """
    # 提取聊天室名称
    chat_name = "common chat"  # 默认值
    if hasattr(request, 'original_description') and request.original_description:
        try:
            # 使用 original_description 作为 screen_data，生成一个临时的 session_id
            import uuid
            temp_session_id = str(uuid.uuid4())
            
            # 调用 chat_name_store 的 read 方法提取聊天室名称
            chat_name = await chat_name_store.read(request.original_description, temp_session_id)
            logger.info(f"从 original_description 提取的聊天室名称: {chat_name}")
            
        except Exception as e:
            logger.error(f"提取聊天室名称时发生错误: {str(e)}")
            chat_name = "common chat"  # 出错时使用默认值
    
    # 返回 data 目录下的 suggestions.json 的内容
    import os

    suggestions_path = os.path.join(os.path.dirname(__file__), "data", "suggestions.json")
    try:
        with open(suggestions_path, "r", encoding="utf-8") as f:
            suggestions_data = json.load(f)
        
        # 在返回的数据中添加 original_description 字段，值为提取到的聊天室名称
        suggestions_data["original_description"] = chat_name
        
    except Exception as e:
        # 如果读取或解析失败，返回错误信息
        return JSONResponse(content={"error": f"无法读取 suggestions.json: {str(e)}"})

    return JSONResponse(content=suggestions_data)


@router.post("/chat")
async def planning_chat(request: PlanningChatRequest) -> StreamingResponse:
    """
    规划聊天API端点 - 流式响应

    Args:
        request: 包含 session_id, stream, query 的请求体

    Returns:
        流式JSON数据
    """

    # 如果有query参数，调用send_msg方法生成新的聊天室数据
    if request.query:
        chat_room = chat_store.send_msg(request.query, request.session_id)
    else:
        # 否则直接获取聊天室数据
        chat_room = chat_store.get_chat_room(request.session_id)

    # 流式返回聊天室数据
    content = f"data: {json.dumps(chat_room)}\n\n"

    return StreamingResponse(iter([content]), media_type="text/event-stream")


@router.post("/completions")
async def planning_completions(request: PlanningRequest, http_request: Request) -> StreamingResponse:
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

    plan_flow_name = http_request.headers.get("plan-flow-name", "")
    planFlow = PlanningTypeEnum.from_string(plan_flow_name)
    if planFlow == PlanningTypeEnum.aTob:
        response_file = response_by_interactions(request.interactions)
        return StreamingResponse(
            stream_generator(request.session_id, request.query, response_file), media_type="text/event-stream"
        )
    else:
        empty_response = {
            "session_id": request.session_id,
            "screens": [
                {
                    "name": "main",
                    "key": "e77b28b0c42672dba773d7564f6dda4a",
                    "state": "active",
                    "title": "Group Travel Planning",
                    "description": "Main screen for collaborative travel planning and coordination.",
                    "icon": "",
                    "focus": request.query,
                    "interaction_value": "",
                    "interaction_template": "",
                    "cards": [],
                }
            ],
        }
        return StreamingResponse(f"data: {json.dumps(empty_response)}\n\n", media_type="text/event-stream")

# /planning-api/api/ai_phone/planning/im_chat_history/save_part
@router.post("/im_chat_history/save_part")
async def save_chat_history(
    request: SaveChatHistoryRequest,
    authorization: str = Header(None)
) -> dict[str, Any]:
    """
    保存聊天历史API端点
curl 'http://localhost:5001/v1.0/invoke/planning-api/method/ai_phone/planning/im_chat_history/save_part' \
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
