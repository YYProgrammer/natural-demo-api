import os
from typing import Any

# from src.static_resources import extract_resources


def get_env(key: str, default: Any = None) -> Any:
    """不区分大小写地获取环境变量

    先尝试原始key，再尝试大写和小写版本的key
    """
    value = os.getenv(key)
    if value is not None:
        return value

    value = os.getenv(key.upper())
    if value is not None:
        return value

    value = os.getenv(key.lower())
    if value is not None:
        return value

    return default


def get_env_bool(key: str, default: bool = False) -> bool:
    """从环境变量获取布尔值，不区分大小写"""
    value = get_env(key)
    if value is None:
        return default
    return value.lower() in ("true", "1", "yes", "y", "t")


def get_env_int(key: str, default: int) -> int:
    """从环境变量获取整数值，不区分大小写"""
    value = get_env(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default
