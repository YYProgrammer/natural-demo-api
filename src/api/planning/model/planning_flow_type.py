from enum import Enum


class PlanningTypeEnum(str, Enum):
    aTob = "a_to_b"
    birthday = "birthday"
    none = ""

    @classmethod
    def from_string(cls, value: str) -> "PlanningTypeEnum":
        """
        将字符串转换为 PlanningTypeEnum 枚举值

        Args:
            value: 输入字符串

        Returns:
            PlanningTypeEnum: 对应的枚举值
            - "a_to_b" -> PlanningTypeEnum.aTob
            - 空字符串或其他任意字符串 -> PlanningTypeEnum.none
        """
        if value == "a_to_b":
            return cls.aTob
        elif value == "birthday":
            return cls.birthday
        else:
            return cls.none
