"""DTO package."""
from pydantic import BaseModel


class ExpertMode(BaseModel):
    """Expert mode configuration object."""

    class Config:
        """Pydantic config inner class."""

        allow_mutation = False

    # * Enable expert mode
    enabled: bool

    # * Command to pass
    masterCommandSeed: str  # noqa: N815
    workerCommandSeed: str  # noqa: N815
