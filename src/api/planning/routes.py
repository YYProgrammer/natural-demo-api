"""
规划API路由

提供规划完成API端点，支持流式响应。
"""

import asyncio
import json

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from enum import Enum

from src.api.planning.model.planning_flow_type import PlanningTypeEnum
from src.api.planning.model.planning_interaction import PlanningInteraction

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
        data_file = os.path.join(current_dir, 'data', response_file)
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
    # 返回 data 目录下的 suggestions.json 的内容
    import os

    suggestions_path = os.path.join(os.path.dirname(__file__), "data", "suggestions.json")
    try:
        with open(suggestions_path, "r", encoding="utf-8") as f:
            suggestions_data = json.load(f)
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

    if request.query == "":
        content = 'data: {"messages": []}\n'
    else:
        content = f'data: {{"messages": [{{"id": 127483413327872, "role": "user", "type": "text", "content": {{"text": "{request.query}"}}}}, {{"id": 127483417473024, "role": "assistant", "type": "text", "content": {{"text": "Developing..."}}}}]}}'

    return StreamingResponse(content, media_type="text/event-stream")


@router.post("/completions")
async def planning_completions(request: PlanningRequest, http_request: Request) -> StreamingResponse:
    """
    规划完成API端点 - 流式响应

    Args:
        request: 包含 session_id, stream, query 的请求体

    Returns:
        流式JSON数据
    """

    plan_flow_name = http_request.headers.get("plan-flow-name", "")
    planFlow = PlanningTypeEnum.from_string(plan_flow_name)
    if planFlow == PlanningTypeEnum.aTob:
        response_file = response_by_interactions(request.interactions)
        return StreamingResponse(stream_generator(request.session_id, request.query, response_file), media_type="text/event-stream")
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
