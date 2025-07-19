from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class PartyPreferences:
    """派对偏好数据类"""

    party_start: str = ""
    party_attendant: str = ""
    party_allergy: str = ""
    party_messages: list[dict[str, Any]] = field(default_factory=list)
    party_user_icons: list[dict[str, Any]] = field(default_factory=list)
    party_meal: str = ""


class PartyPreferencesStore:
    """
    派对偏好存储类

    管理各个session的派对偏好数据。
    """

    def __init__(self):
        """初始化派对偏好存储"""
        self._party_preferences: Dict[str, PartyPreferences] = {}

        self._progressive_messages = self._generate_progressive_messages()

    def _generate_progressive_messages(self) -> list[list[dict[str, Any]]]:
        """生成五组递增的消息数组"""
        base_messages = [
            {
                "content": "大家都来参加生日派对吧！🎉",
                "is_from_current_user": True,
                "timestamp": "2:00 PM",
                "user_name": "小明",
            },
            {
                "content": "太好了！我会准时到的",
                "is_from_current_user": False,
                "timestamp": "2:05 PM",
                "user_name": "小红",
            },
            {
                "content": "需要我带什么东西吗？",
                "is_from_current_user": False,
                "timestamp": "2:10 PM",
                "user_name": "小李",
            },
            {
                "content": "带点饮料就行，蛋糕我已经订好了",
                "is_from_current_user": True,
                "timestamp": "2:15 PM",
                "user_name": "小明",
            },
            {
                "content": "期待今晚的派对！🎂🎈",
                "is_from_current_user": False,
                "timestamp": "2:20 PM",
                "user_name": "小王",
            },
        ]

        # 生成五组递增的消息数组
        progressive_messages = []
        for i in range(1, 6):
            progressive_messages.append(base_messages[:i])

        return progressive_messages

    def get_progressive_messages(self, index: int) -> list[dict[str, Any]]:
        """获取指定索引的递增消息数组"""
        if 0 <= index < len(self._progressive_messages):
            return self._progressive_messages[index]
        return []

    def has_preferences(self, session_id: str) -> bool:
        """判断偏好数据是否存在"""
        return session_id in self._party_preferences

    def get_party_preferences(self, session_id: str) -> PartyPreferences:
        """获取派对偏好数据"""
        return self._party_preferences.get(session_id, PartyPreferences())

    def set_party_preferences(self, session_id: str, party_preferences: PartyPreferences) -> None:
        """设置派对偏好数据"""
        self._party_preferences[session_id] = party_preferences

    def set_party_start_time(self, session_id: str, start_time: str) -> None:
        """设置派对开始时间"""
        if session_id not in self._party_preferences:
            self._party_preferences[session_id] = PartyPreferences()
        self._party_preferences[session_id].party_start = start_time

    def set_party_attendant(self, session_id: str, attendant: str) -> None:
        """设置派对出席人员"""
        if session_id not in self._party_preferences:
            self._party_preferences[session_id] = PartyPreferences()
        self._party_preferences[session_id].party_attendant = attendant

    def set_party_allergy(self, session_id: str, allergy: str) -> None:
        """设置派对忌口信息"""
        if session_id not in self._party_preferences:
            self._party_preferences[session_id] = PartyPreferences()
        self._party_preferences[session_id].party_allergy = allergy

    def get_party_start_time(self, session_id: str) -> str:
        """获取派对开始时间"""
        return self.get_party_preferences(session_id).party_start

    def get_party_attendant(self, session_id: str) -> str:
        """获取派对出席人员"""
        return self.get_party_preferences(session_id).party_attendant

    def get_party_allergy(self, session_id: str) -> str:
        """获取派对忌口信息"""
        return self.get_party_preferences(session_id).party_allergy

    def clear_session(self, session_id: str) -> None:
        """清除指定 session 的偏好数据"""
        if session_id in self._party_preferences:
            del self._party_preferences[session_id]

    def update_party_preferences(self, session_id: str, **kwargs) -> None:
        """更新派对偏好数据的部分字段"""
        if session_id not in self._party_preferences:
            self._party_preferences[session_id] = PartyPreferences()

        preferences = self._party_preferences[session_id]
        for key, value in kwargs.items():
            if hasattr(preferences, key):
                setattr(preferences, key, value)

    def get_party_messages(self, session_id: str) -> list[dict[str, Any]]:
        """获取派对消息"""
        return self.get_party_preferences(session_id).party_messages

    def get_party_user_icons(self, session_id: str) -> list[dict[str, Any]]:
        """获取派对用户图标"""
        return self.get_party_preferences(session_id).party_user_icons

    def set_party_messages(self, session_id: str, messages: list[dict[str, Any]]) -> None:
        """设置派对消息"""
        if session_id not in self._party_preferences:
            self._party_preferences[session_id] = PartyPreferences()
        self._party_preferences[session_id].party_messages = messages

    def set_party_user_icons(self, session_id: str, user_icons: list[dict[str, Any]]) -> None:
        """设置派对用户图标"""
        if session_id not in self._party_preferences:
            self._party_preferences[session_id] = PartyPreferences()
        self._party_preferences[session_id].party_user_icons = user_icons

    def get_party_meal(self, session_id: str) -> str:
        """获取派对餐食"""
        return self.get_party_preferences(session_id).party_meal

    def set_party_meal(self, session_id: str, meal: str) -> None:
        """设置派对餐食"""
        if session_id not in self._party_preferences:
            self._party_preferences[session_id] = PartyPreferences()
        self._party_preferences[session_id].party_meal = meal


# 创建并导出PartyPreferencesStore实例
party_preferences_store = PartyPreferencesStore()
