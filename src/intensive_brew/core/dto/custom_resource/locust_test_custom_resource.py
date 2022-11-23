"""Locust Test custom resource DTO package."""
from pydantic import BaseModel, Field

from intensive_brew.core.dto.custom_resource.metadata import Metadata
from intensive_brew.core.dto.custom_resource.spec import Spec


class LocustTest(BaseModel):
    """Locust Test custom resource DTO class."""

    class Config:
        """Pydantic config class."""

        frozen = True

    api_version: str = Field("locust.io/v1", alias="apiVersion")
    kind: str = "LocustTest"
    metadata: Metadata
    spec: Spec
