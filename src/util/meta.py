from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Meta(Exception):
    name: str
    message: str = ""
    data: Optional[Any] = None

    def __str__(self) -> str:
        return f"{self.name}: {self.message}"
