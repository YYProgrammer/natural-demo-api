"""
规划API路由

提供规划完成API端点，支持流式响应。
"""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Header, Request

from src.api.chathistory.models.save_part import SaveChatHistoryRequest
from src.api.planning.model.planning_flow_type import PlanningTypeEnum
from src.services.notification.notification_service import notification_service
from src.util.request_util import parse_plan_flow_name_from_headers

# from src.base.util.log_util import logger

router = APIRouter(prefix="/remote", tags=["remote"])


@router.post("/im_chat_history/save_part")
async def save_chat_history(
    request: SaveChatHistoryRequest, http_request: Request, authorization: str = Header(...)
) -> dict[str, Any]:
    """
    保存聊天历史API端点
curl 'http://localhost:5001/v1.0/invoke/planning-api/method/remote/im_chat_history/save_part' \
-X POST \
-H 'authorization: token c77eb8509f7d6bfa3db8af4d152e27dcb2b32c64' \
-H 'content-type: application/json' \
--data-raw '{"data":{"chat_name":"王和平, 李菊巨, Hilman obuy, KevinVasa","messages":[{"content":"Test","is_from_current_user":true,"timestamp":"3:07 PM","user_name":null},{"content":"Hi","is_from_current_user":false,"timestamp":"7:09 PM","user_name":"王和平"}]},"is_oldest_reached":false,"package_name":"jp.naver.line.android","session_id":"xxx","task_id":"111222","type":"AMChatHistoryMsg"}'
    """
    # 获取并记录 token
    if authorization:
        # 处理 "token xxx" 格式的 authorization header
        if authorization.startswith("token "):
            token = authorization[6:]  # 去掉 "token " 前缀
        else:
            token = authorization

    planFlow = parse_plan_flow_name_from_headers(http_request.headers)
    if planFlow != PlanningTypeEnum.birthday:
        await notification_service.handle_message(request.data.messages, request.session_id, token)

    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
    }
