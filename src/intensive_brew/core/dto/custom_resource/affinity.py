"""Locust Test custom resource DTO package."""

from pydantic import BaseModel, Field

from intensive_brew.core.dto.custom_resource.node_affinity import NodeAffinity


class Affinity(BaseModel):
    """Locust Test custom resource Affinity class."""

    class Config:
        """Pydantic config class."""

        frozen = True

    node_affinity: NodeAffinity | None = Field(None, alias="nodeAffinity")
