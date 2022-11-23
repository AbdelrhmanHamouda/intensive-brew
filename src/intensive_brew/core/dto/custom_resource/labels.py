"""Locust Test custom resource DTO package."""

from pydantic import BaseModel


class Labels(BaseModel):
    """Locust Test custom resource Labels class."""

    class Config:
        """Pydantic config class."""

        frozen = True

    master: dict[str, str] = {}
    worker: dict[str, str] = {}
