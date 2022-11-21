"""DTO package."""

from pydantic import BaseModel

from intensive_brew.core.dto.test_config import TestConfig


class Configuration(BaseModel):
    """Main object for the configuration."""

    class Config:
        """Pydantic config inner class."""

        frozen = True

    test_key: dict[str, TestConfig]
