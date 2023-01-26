"""Locust Test custom resource DTO package."""

from pydantic import BaseModel, Field


class NodeAffinity(BaseModel):
    """Locust Test custom resource NodeAffinity class."""

    class Config:
        """Pydantic config class."""

        frozen = True

    required_during_scheduling_ignored_during_execution: dict[str, str] = Field({}, alias="requiredDuringSchedulingIgnoredDuringExecution")
