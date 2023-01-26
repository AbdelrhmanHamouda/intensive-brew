"""Locust Test custom resource DTO package."""
from typing import Literal

from pydantic import BaseModel


class Toleration(BaseModel):
    """Locust Test custom resource Tolerations class."""

    class Config:
        """Pydantic config class."""

        frozen = True

    key: str
    operator: Literal["Exists", "Equal"]
    effect: Literal["NoSchedule", "PreferNoSchedule", "NoExecute"]
    value: str | None = None
