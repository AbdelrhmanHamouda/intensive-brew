"""DTO package."""

from pydantic import BaseModel

from intensive_brew.core.dto.yaml.test_config import TestConfig


class Configuration(BaseModel):
    """Main object for the configuration."""

    class Config:
        """Pydantic config inner class."""

        frozen = True

    configurations: dict[str, TestConfig]
