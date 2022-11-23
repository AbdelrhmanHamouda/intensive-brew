"""Locust Test custom resource DTO package."""
from pydantic import BaseModel, Field

from intensive_brew.core.dto.custom_resource.annotations import Annotations
from intensive_brew.core.dto.custom_resource.labels import Labels


class Spec(BaseModel):
    """Locust Test custom resource Spec class."""

    class Config:
        """Pydantic config class."""

        frozen = True

    image: str = "locustio/locust:latest"
    labels: Labels | None = None
    annotations: Annotations | None = None
    master_command_seed: str = Field(..., alias="masterCommandSeed")
    worker_command_seed: str = Field(..., alias="workerCommandSeed")
    worker_replicas: int = Field(5, alias="workerReplicas")
    config_map: str | None = Field(None, alias="configMap")
