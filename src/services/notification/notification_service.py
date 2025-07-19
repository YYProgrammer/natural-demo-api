import base64
from typing import Any

import aiohttp

from src.api.chathistory.models.save_part import ChatMessage
from src.api.notification.models.request import Notification, NotificationBody
from src.base.util.log_util import logger
from src.store.chat.chat_name_store import chat_name_store


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

    async def handle_message(self, messages: list[ChatMessage], session_id: str, channel_name: str):
        """
        处理消息的主方法

        Args:
            message_body: 消息体
            channel_name: 频道名称（通常是token）
        """

        logger.info(f"handle_message: {messages}, {session_id}, {channel_name}")

        if messages:
            last_message = messages[-1]
            if "late" in last_message.content.lower():
                logger.info(f"消息包含late，处理: {last_message.content}")
                await self.finish_request_chat_history(session_id, channel_name)
                chat_name = chat_name_store.get_chat_name(session_id)
                logger.info(f"handle_message chat_name: {chat_name}")
                await self.phone_notification(session_id, channel_name, chat_name)
                return

    async def send_notification(self, notification: Notification, token: str) -> None:
        """
        发送通知
        """
        # 提取token
        if token.startswith("token "):
            token = token[6:]  # 移除 "token " 前缀
        else:
            token = token

        await self.process_message(notification, token)

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

        notification = Notification(
            id="108138381078528",
            name="AMChatHistoryMsg",
            created=1749686833,
            arrival=1749686833,
            body=NotificationBody(
                type="AMChatHistoryMsg",
                package_name="jp.naver.line.android",
                session_id=session_id,
                task_id="request_chat_history",
                data={"chat_name": chat_name, "screen_count": 5},
            ),
        )

        await self.send_notification(notification, token)

    async def finish_request_chat_history(self, session_id: str, token: str) -> None:
        """
        停止请求聊天历史

        Args:
            session_id: 会话ID
            token: 用户token
        """
        notification = Notification(
            id="108138381078528",
            name="AMFinishMsg",
            created=1749686833,
            arrival=1749686833,
            body=NotificationBody(
                type="AMFinishMsg",
                package_name="jp.naver.line.android",
                session_id=session_id,
                task_id="finish_request_chat_history",
            ),
        )

        await self.send_notification(notification, token)

    async def phone_notification(self, session_id: str, token: str, chat_name: str) -> None:
        """
        发送手机通知

        Args:
            session_id: 会话ID
            token: 用户token
        """
        notification = Notification(
            id="108138381078528",
            name="PhoneNotificationMsg",
            created=1749686833,
            arrival=1749686833,
            body=NotificationBody(
                type="PhoneNotificationMsg",
                session_id=session_id,
                data={
                    "title": "Your friend will be late by 2 hours",
                    "detail": "Leave by 3pm to get to Shinjuku at 4pm",
                    "interactions": [
                        {
                            "type": "onTapPhoneNotification",
                            "title": "Your friend will be late by 2 hours",
                            "description": "Leave by 3pm to get to Shinjuku at 4pm",
                            "value": {"chat_name": chat_name},
                            "relation_key": "",
                        }
                    ],
                    "original_description": "",
                },
            ),
        )

        await self.send_notification(notification, token)

    async def calendar_saved_phone_notification(self, session_id: str, token: str) -> None:
        """
        发送手机通知

        Args:
            session_id: 会话ID
            token: 用户token
        """
        notification = Notification(
            id="108138381078528",
            name="PhoneNotificationMsg",
            created=1749686833,
            arrival=1749686833,
            body=NotificationBody(
                type="PhoneNotificationMsg",
                session_id=session_id,
                data={
                    "title": "Calendar saved",
                    "detail": "Calendar saved",
                    "interactions": [],
                    "original_description": "",
                },
            ),
        )

        await self.send_notification(notification, token)

    async def send_chat_message(
        self, session_id: str, chat_name: str, message_list: list[str], token: str, task_id: str = ""
    ) -> None:
        """
        发送聊天消息

        Args:
            session_id: 会话ID
            chat_name: 聊天名称
            message_list: 消息列表
            token: 用户token
            task_id: 任务ID（可选）
        """
        notification = Notification(
            id="108138381078528",
            name="AMSentChatMsg",
            created=1749686833,
            arrival=1749686833,
            body=NotificationBody(
                type="AMSentChatMsg",
                package_name="jp.naver.line.android",
                session_id=session_id,
                task_id=task_id,
                data={
                    "chat_name": chat_name,
                    "message_list": message_list,
                },
            ),
        )

        await self.send_notification(notification, token)

    async def send_chat_hide(
        self, session_id: str, chat_name: str, message_list: list[str], token: str, task_id: str = ""
    ) -> None:
        """
        发送聊天消息

        Args:
            session_id: 会话ID
            chat_name: 聊天名称
            message_list: 消息列表
            token: 用户token
            task_id: 任务ID（可选）
        """
        notification = Notification(
            id="108138381078528",
            name="PlanningChatHideMsg",
            created=1749686833,
            arrival=1749686833,
            body=NotificationBody(
                type="PlanningChatHideMsg",
                session_id=session_id,
            ),
        )

        await self.send_notification(notification, token)

    async def send_plan_reload(
        self, session_id: str, chat_name: str, message_list: list[str], token: str, task_id: str = ""
    ) -> None:
        """
        发送聊天消息

        Args:
            session_id: 会话ID
            chat_name: 聊天名称
            message_list: 消息列表
            token: 用户token
            task_id: 任务ID（可选）
        """
        notification = Notification(
            id="108138381078528",
            name="PlanningReloadMsg",
            created=1749686833,
            arrival=1749686833,
            body=NotificationBody(
                type="PlanningReloadMsg",
                session_id=session_id,
                interactions=[
                    {
                        "type": "onBirthdayPlanningReload",
                        "title": "Birthday Planning Reload",
                        "description": "Birthday Planning Reload",
                        "value": {},
                        "relation_key": "",
                    }
                ],
            ),
        )

        await self.send_notification(notification, token)

    async def send_plan_reload_chat_hide(self, session_id: str, token: str) -> None:
        """
        发送聊天消息
        """
        await self.send_plan_reload(session_id, "common chat", [], token)
        await self.send_chat_hide(session_id, "common chat", [], token)

    async def birthday_agent_update(self, session_id: str, token: str, interaction_type: str) -> None:
        """
        发送生日 agent 更新通知
        """
        notification = Notification(
            id="108138381078528",
            name="PlanningReloadMsg",
            created=1749686833,
            arrival=1749686833,
            body=NotificationBody(
                type="PlanningReloadMsg",
                session_id=session_id,
                interactions=[
                    {
                        "type": interaction_type,
                        "title": "",
                        "description": "",
                        "value": {},
                        "relation_key": "",
                    }
                ],
            ),
        )

        await self.send_notification(notification, token)

    async def birthday_agent_update_v2(self, session_id: str, token: str, messages: list[dict[str, Any]]) -> None:
        """
        发送生日 agent 更新通知
        """
        notification = Notification(
            id="108138381078528",
            name="ChatHistoryLatestMsg",
            created=1749686833,
            arrival=1749686833,
            body=NotificationBody(
                is_oldest_reached=True,
                type="ChatHistoryLatestMsg",
                session_id=session_id,
                package_name="jp.naver.line.android",
                data={
                    "chat_name": "王和平, 李菊巨, Hilman obuy, KevinVasa",
                    "user_icons": [{"user_name": "王和平", "user_icon": ""}],
                    "messages": messages,
                },
            ),
        )

        await self.send_notification(notification, token)

    async def birthday_agent_done(self, session_id: str, token: str) -> None:
        """
        发送生日 agent 完成通知
        """
        notification = Notification(
            id="108138381078528",
            name="PlanningReloadMsg",
            created=1749686833,
            arrival=1749686833,
            body=NotificationBody(
                type="PlanningReloadMsg",
                session_id=session_id,
                interactions=[
                    {
                        "type": "onBirthdayPlanningDone",
                        "title": "",
                        "description": "",
                        "value": {},
                        "relation_key": "",
                    }
                ],
            ),
        )

        await self.send_notification(notification, token)


# 创建并导出实例
notification_service = NotificationService()
