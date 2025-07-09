from typing import Any, Optional

from pydantic import BaseModel


class PlanningInteraction(BaseModel):
    type: str = ""
    title: str = ""
    description: str = ""
    value: Optional[Any] = None
    relation_key: str = ""
