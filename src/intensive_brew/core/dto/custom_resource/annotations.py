"""Locust Test custom resource DTO package."""

from pydantic import BaseModel


class Annotations(BaseModel):
    """Locust Test custom resource Annotations class."""

    class Config:
        """Pydantic config class."""

        frozen = True

    master: dict[str, str] = {}
    worker: dict[str, str] = {}
