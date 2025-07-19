import asyncio

from src.api.planning.model.planning_interaction import PlanningInteraction
from src.services.notification.notification_service import notification_service
from src.store.birthday.party_preferences_store import party_preferences_store
from src.util.request_util import get_next_interaction_type


class BirthdayService:
    """生日流程服务"""

    def __init__(self):
        """初始化服务"""
        self._timer_task = None
        self._done_task = None

    def updateAgent(self, session_id: str, token: str, interaction: PlanningInteraction):
        """非阻塞的异步定时器更新 agent"""
        # 取消已有的定时器任务
        if self._timer_task is not None and not self._timer_task.done():
            self._timer_task.cancel()

        next_interaction_type = get_next_interaction_type(interaction)

        if len(next_interaction_type) > 0:
            # 启动新的非阻塞定时器任务
            self._timer_task = asyncio.create_task(self._delayed_update(session_id, token, next_interaction_type))

    def agent_done_delayed(self, session_id: str, token: str):
        """每秒调用一次birthday_agent_update_v2，调用5次后调用birthday_agent_done"""
        # 取消已有的完成任务
        if self._done_task is not None and not self._done_task.done():
            self._done_task.cancel()

        # 启动新的非阻塞延迟任务，每秒调用一次，共5次
        self._done_task = asyncio.create_task(self._delayed_update_sequence(session_id, token))

    async def _delayed_update(self, session_id: str, token: str, interaction_type: str):
        """延迟更新的内部方法"""
        await asyncio.sleep(5.0)
        await notification_service.birthday_agent_update(session_id, token, interaction_type)

    async def _delayed_update_sequence(self, session_id: str, token: str):
        # 每2秒调用一次 birthday_agent_update_v2，共5次，每次使用不同的消息数组
        for i in range(5):
            await asyncio.sleep(2.0)

            # 从 party_preferences_store 获取当前索引的消息数组
            messages = party_preferences_store.get_progressive_messages(i)
            party_preferences_store.set_party_messages(session_id, messages)

            # 调用 birthday_agent_update_v2
            await notification_service.birthday_agent_update_v2(session_id, token, messages)

        # 5次调用完成后，调用 birthday_agent_done
        await notification_service.birthday_agent_done(session_id, token)


birthday_service = BirthdayService()
