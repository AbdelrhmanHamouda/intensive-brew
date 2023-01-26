"""DTO package."""
from pydantic import BaseModel, validator

from intensive_brew.core.dto.custom_resource.affinity import Affinity
from intensive_brew.core.dto.custom_resource.annotations import Annotations
from intensive_brew.core.dto.custom_resource.labels import Labels
from intensive_brew.core.dto.custom_resource.toleration import Toleration
from intensive_brew.core.dto.utils.validator_utils import is_expert
from intensive_brew.core.dto.yaml.expert_mode import ExpertMode
from intensive_brew.core.dto.yaml.vanilla_specs import VanillaSpecs


class TestConfig(BaseModel):
    """Main test configuration."""

    # Needed so the pytest runner ignore this class from test collection
    __test__ = False

    # * Expert mode
    expert_mode: ExpertMode | None = None

    # * Entry point script
    entry_point: str | None = None

    # * Custom load shape support
    custom_load_shapes: bool | None = False

    # * Vanilla load requirements
    vanilla_specs: VanillaSpecs | None = None

    # * Locust container image
    image: str | None = "locustio/locust:latest"

    # * Worker replicas
    worker_replicas: int | None = 5

    # * Test configuration map
    configmap: str | None = None

    # * Labels
    labels: Labels | None = None

    # * Annotations
    annotations: Annotations | None = None

    # * Taint tolerations
    tolerations: list[Toleration] | None = None

    # * Affinity
    affinity: Affinity | None = None

    @validator("entry_point", always=True)
    def check_entry_point(cls, param_value: str, values):  # type: ignore[no-untyped-def] # noqa: N805
        """Validate entry point if expert mode is not enabled."""
        if not is_expert(values) and param_value is None:
            raise ValueError("The field 'entry_point' must be provided.")
        return param_value

    @validator("vanilla_specs", always=True)
    def check_vanilla_specs(cls, param_value: VanillaSpecs, values):  # type: ignore[no-untyped-def] # noqa: N805
        """Validate vanilla specs if expert mode is not enabled or no custom load shapes."""
        if (not is_expert(values)) and (values["custom_load_shapes"] is False) and (param_value is None):
            raise ValueError("The section 'vanilla_specs' must be provided.")
        return param_value
