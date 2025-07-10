import base64

import aiohttp

from src.api.chathistory.models.save_part import ChatMessage
from src.api.notification.models.request import Notification, NotificationBody
from src.base.util.log_util import logger


def filter_none_values(data):
    """
    递归过滤字典中的None值

    Args:
        data: 要过滤的数据（字典、列表或基本类型）

    Returns:
        过滤后的数据，不包含None值
    """
    if isinstance(data, dict):
        return {k: filter_none_values(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [filter_none_values(item) for item in data if item is not None]
    else:
        return data


channel_name = "Notification"
ably_api_key = "hhtFVg.xSj3PQ:NW0ptsU7xatvE5jdlfmt5j-z74LEzSShrqXC3MfqXek"


class NotificationService:
    """通知处理服务"""

    def __init__(self):
        """初始化服务"""
        self._requested_sessions = set()  # 用于跟踪已请求的session_id

    async def _publish_via_ably_http(self, channel_name: str, notification: Notification) -> None:
        """
        通过HTTP直接调用Ably REST API发布消息
        """
        try:
            data = notification.model_dump()

            # 过滤None值
            data = filter_none_values(data)

            logger.info(f"通过HTTP发布消息到频道: {channel_name}, data: {data}")

            # 构建HTTP请求
            url = f"https://rest.ably.io/channels/{channel_name}/messages"

            # 使用Base64编码的API key进行Basic认证（避免冒号问题）
            api_key_encoded = base64.b64encode(ably_api_key.encode()).decode()
            headers = {"Content-Type": "application/json", "Authorization": f"Basic {api_key_encoded}"}

            payload = {"name": "Notification", "data": data}

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 201:
                        logger.info(f"HTTP发布成功 - Channel: {channel_name}")
                    else:
                        error_text = await response.text()
                        logger.error(
                            f"HTTP发布失败 - Channel: {channel_name}, Status: {response.status}, Error: {error_text}"
                        )
                        raise Exception(f"HTTP发布失败: {response.status} - {error_text}")

        except Exception as e:
            logger.error(f"HTTP发布消息时发生错误 - Channel: {channel_name}, Error: {e}")
            raise

    async def process_message(self, message_body: Notification, channel_name: str | None = None) -> dict:
        """
        处理消息的主方法

        Args:
            message_body: 消息体
            channel_name: 频道名称（通常是token）

        Returns:
            处理结果字典
        """
        try:
            data = message_body.model_dump()

            # 过滤None值
            data = filter_none_values(data)

            logger.info(f"开始处理消息: {data}")

            # 如果有频道名称，发布到Ably
            if channel_name:
                await self._publish_via_ably_http(channel_name, message_body)

            return {"success": True, "message_id": message_body.id, "channel_name": channel_name, "data": data}

        except Exception as e:
            logger.error(f"处理消息时发生错误: {e}, Type: {type(e).__name__}")
            return {
                "success": False,
                "error": str(e),
                "message_id": getattr(message_body, "id", None),
                "channel_name": channel_name,
            }

    def handle_message(self, messages: list[ChatMessage], channel_name: str | None = None):
        """
        处理消息的主方法

        Args:
            message_body: 消息体
            channel_name: 频道名称（通常是token）
        """
        pass

    async def request_chat_history(self, session_id: str, chat_name: str, token: str) -> None:
        """
        请求聊天历史

        Args:
            session_id: 会话ID
            token: 用户token
        """
        # 检查是否已经请求过该session_id
        if session_id in self._requested_sessions:
            logger.info(f"Session {session_id} 已经请求过聊天历史，跳过重复请求")
            return

        # 标记该session_id已请求
        self._requested_sessions.add(session_id)

        # 提取token
        if token.startswith("token "):
            token = token[6:]  # 移除 "token " 前缀
        else:
            token = token

        req_notification = Notification(
            id="108138381078528",
            name="AMChatHistoryMsg",
            created=1749686833,
            arrival=1749686833,
            body=NotificationBody(
                type="AMChatHistoryMsg",
                package_name="jp.naver.line.android",
                session_id=session_id,
                task_id="",
                data={"chat_name": chat_name, "screen_count": 5},
            ),
        )

        await self.process_message(req_notification, token)


# 创建并导出实例
notification_service = NotificationService()
