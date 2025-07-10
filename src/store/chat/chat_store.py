"""
聊天存储模块

管理聊天室数据，包括消息的存储和检索。
"""

from typing import Any, Dict


class ChatStore:
    """
    聊天存储类

    管理各个session的聊天室数据，支持消息的存储和检索。
    """

    def __init__(self):
        """初始化聊天存储"""
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def get_chat_room(self, session_id: str) -> Dict[str, Any]:
        """
        根据session_id获取聊天室数据

        Args:
            session_id: 会话ID

        Returns:
            聊天室数据字典
        """
        if session_id not in self._sessions:
            # 首次获取，初始化聊天室数据
            self._sessions[session_id] = {
                "messages": [
                    {"id": 127598664749056, "role": "user", "type": "text", "content": {"text": "Hi"}},
                    {"id": 127598668926976, "role": "assistant", "type": "text", "content": {"text": "I'm thinking"}},
                ]
            }

        return self._sessions[session_id]

    def _generate_new_id(self, session_id: str) -> int:
        """
        生成新的消息ID

        Args:
            session_id: 会话ID

        Returns:
            新的消息ID
        """
        chat_room = self.get_chat_room(session_id)
        if not chat_room["messages"]:
            return 127598664749056  # 默认起始ID

        last_message = chat_room["messages"][-1]
        return last_message["id"] + 1

    def send_msg(self, query: str, session_id: str) -> Dict[str, Any]:
        """
        发送消息到指定会话

        Args:
            query: 用户查询内容
            session_id: 会话ID

        Returns:
            更新后的聊天室数据
        """
        chat_room = self.get_chat_room(session_id)

        # 生成用户消息ID
        user_msg_id = self._generate_new_id(session_id)

        # 创建用户消息
        user_message = {"id": user_msg_id, "role": "user", "type": "text", "content": {"text": query}}

        # 添加用户消息
        chat_room["messages"].append(user_message)

        # 生成助手消息ID
        assistant_msg_id = user_msg_id + 1

        # 创建助手消息
        assistant_message = {
            "id": assistant_msg_id,
            "role": "assistant",
            "type": "text",
            "content": {"text": "I'm thinking"},
        }

        # 添加助手消息
        chat_room["messages"].append(assistant_message)

        return chat_room


# 创建并导出ChatStore实例
chat_store = ChatStore()
