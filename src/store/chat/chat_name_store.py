"""
聊天名称存储模块

管理聊天室名称的提取和存储。
"""

import json
from typing import Any, Dict

import httpx

from src.base.util.log_util import logger


class ChatNameStore:
    """
    聊天名称存储类

    管理各个session的聊天室名称，支持从屏幕数据中提取聊天室名称。
    """

    def __init__(self):
        """初始化聊天名称存储"""
        self._chat_names: Dict[str, str] = {}

    async def read(self, screen_data: str, session_id: str) -> str:
        """
        从屏幕数据中提取聊天室名称并保存

        Args:
            screen_data: 聊天室的手机屏幕json数据
            session_id: 会话ID

        Returns:
            提取到的聊天室名称
        """
        try:
            # 准备API请求数据
            api_url = "https://cerebras-proxy.brain.loocaa.com:1443/v1/chat/completions"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer DlJYSkMVj1x4zoe8jZnjvxfHG6z5yGxK"
            }
            
            payload = {
                "model": "llama-3.3-70b",
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个安卓屏幕屏幕信息json数据阅读的专家，用户会传入的一个聊天页面的安卓屏幕json数据，你需要读取出这个屏幕里对应的聊天室的标题。如果传入的内容是chat_name: xxxx这种格式，则chat_name后面的内容就是聊天室标题。你的输出只有聊天室标题，不要输入其它内容"
                    },
                    {
                        "role": "user",
                        "content": screen_data
                    }
                ]
            }

            # 发送API请求
            async with httpx.AsyncClient() as client:
                response = await client.post(api_url, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                
                # 解析响应
                response_data = response.json()
                
                # 提取聊天室名称
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    chat_name = response_data["choices"][0]["message"]["content"].strip()
                    
                    # 保存聊天室名称
                    self._chat_names[session_id] = chat_name
                    
                    logger.info(f"成功提取聊天室名称: {chat_name} (session_id: {session_id})")
                    return chat_name
                else:
                    logger.error(f"API响应中未找到聊天室名称: {response_data}")
                    return "common chat"
                    
        except httpx.RequestError as e:
            logger.error(f"API请求失败: {e}")
            return "common chat"
        except httpx.HTTPStatusError as e:
            logger.error(f"API请求返回错误状态: {e.response.status_code} - {e.response.text}")
            return "common chat"
        except json.JSONDecodeError as e:
            logger.error(f"API响应JSON解析失败: {e}")
            return "common chat"
        except Exception as e:
            logger.error(f"提取聊天室名称时发生未知错误: {e}")
            return "common chat"

    def get_chat_name(self, session_id: str) -> str:
        """
        根据session_id获取聊天室名称

        Args:
            session_id: 会话ID

        Returns:
            聊天室名称，如果未找到则返回"common chat"
        """
        return self._chat_names.get(session_id, "common chat")

    def has_chat_name(self, session_id: str) -> bool:
        """
        检查是否存在指定session的聊天室名称

        Args:
            session_id: 会话ID

        Returns:
            如果存在则返回True，否则返回False
        """
        return session_id in self._chat_names

    def clear_chat_name(self, session_id: str) -> None:
        """
        清除指定session的聊天室名称

        Args:
            session_id: 会话ID
        """
        if session_id in self._chat_names:
            del self._chat_names[session_id]
            logger.info(f"已清除聊天室名称 (session_id: {session_id})")

    def get_all_chat_names(self) -> Dict[str, str]:
        """
        获取所有聊天室名称

        Returns:
            包含所有session_id和对应聊天室名称的字典
        """
        return self._chat_names.copy()


# 创建并导出ChatNameStore实例
chat_name_store = ChatNameStore() 