"""Locust Test custom resource DTO package."""

from pydantic import BaseModel


class Metadata(BaseModel):
    """Locust Test custom resource Metadata class."""

    class Config:
        """Pydantic config class."""

        frozen = True

    name: str
