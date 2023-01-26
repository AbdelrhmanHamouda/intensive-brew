"""Test package."""
import logging
import re

from intensive_brew.core.custom_resource.utils.constants import (
    CUSTOM_LOAD_SHAPE_COMMAND_TEMPLATE,
    DEFAULT_CONTAINER_TEST_DIR,
    VANILLA_SPECS_COMMAND_TEMPLATE,
)
from intensive_brew.core.custom_resource.utils.helpers import Helpers
from intensive_brew.core.dto.custom_resource.affinity import Affinity
from intensive_brew.core.dto.custom_resource.metadata import Metadata
from intensive_brew.core.dto.custom_resource.node_affinity import NodeAffinity
from intensive_brew.core.dto.custom_resource.spec import Spec
from intensive_brew.core.dto.custom_resource.toleration import Toleration
from intensive_brew.core.dto.yaml.expert_mode import ExpertMode
from intensive_brew.core.dto.yaml.test_config import TestConfig
from intensive_brew.core.dto.yaml.vanilla_specs import VanillaSpecs

DEFAULT_RUN_TIME = "55h"
DEFAULT_SPAWN_RATE = 20
DEFAULT_TEST_USERS = 10000
DEFAULT_ENTRY_POINT = "src/my_test.py"
DEFAULT_TARGET_HOST = "http://localhost:8080"
DEFAULT_EXPERT_MODE_SEED_CMD = "--locustfile src/my_test.py --u 1000"


def prepare_reference_cr_configuration(configuration: TestConfig) -> Spec:
    """Prepare a reference custom resource configuration."""
    # Generate locust command seeds
    master_command_seed = Helpers._generate_master_command_seed(configuration)
    worker_command_seed = Helpers._generate_worker_command_seed(configuration)

    # Calculate replicas
    worker_replicas = configuration.worker_replicas

    # Get image path
    image = configuration.image

    # Get Configuration map
    config_map = configuration.configmap

    # Get labels
    labels = configuration.labels

    # Get annotations
    annotations = configuration.annotations

    # Get affinity
    affinity = configuration.affinity

    # Get taint tolerations
    tolerations = configuration.tolerations

    return Spec(
        masterCommandSeed=master_command_seed,
        workerCommandSeed=worker_command_seed,
        workerReplicas=worker_replicas,  # type: ignore[arg-type]
        image=image,  # type: ignore[arg-type]
        configMap=config_map,
        labels=labels,
        annotations=annotations,
        affinity=affinity,
        tolerations=tolerations,
    )


def prepare_test_config(mode: str = "custom") -> TestConfig:
    """
    Create a predictable test configuration.

    Create a `TestConfig` object based on the `mode` parameter. Supported modes:
    - custom >> Team object with custom_load_shape enabled
    - expert >> Team object with expert_mode object enabled and populated
    - vanilla >> Team Object with vanilla specs
    :param mode: operation mode. Values: custom, expert or vanilla
    :return: TestConfig object
    """
    # Expert mode
    if mode.lower() == "expert":
        test_config = TestConfig(
            expert_mode=ExpertMode(
                enabled=True, masterCommandSeed=DEFAULT_EXPERT_MODE_SEED_CMD, workerCommandSeed=DEFAULT_EXPERT_MODE_SEED_CMD
            )
        )
    # Custom load  mode
    elif mode.lower() == "custom":
        test_config = TestConfig(entry_point=DEFAULT_ENTRY_POINT, custom_load_shapes=True)
    # Vanilla mode
    elif mode.lower() == "vanilla":
        test_config = TestConfig(
            entry_point=DEFAULT_ENTRY_POINT,
            vanilla_specs=VanillaSpecs(
                users=DEFAULT_TEST_USERS,
                spawn_rate=DEFAULT_SPAWN_RATE,
                run_time=DEFAULT_RUN_TIME,
                target_host=DEFAULT_TARGET_HOST,  # type: ignore[arg-type]
            ),
        )
    else:
        raise RuntimeError(f"Invalid `mode` selected. Supported modes are:['custom', 'expert', 'vanilla'], Selected mode: {mode}")

    logging.debug(f"Generated Team config based on {mode=}, is {test_config}")
    return test_config


def prepare_test_config_with_node_affinity(affinity_map: dict[str, str]) -> TestConfig:
    """
    Create a predictable test configuration.

    Create a `TestConfig` object with node affinity information

    :param affinity_map:
    :return:
    """
    affinity = Affinity(nodeAffinity=NodeAffinity(requiredDuringSchedulingIgnoredDuringExecution=affinity_map))
    test_config = TestConfig(entry_point=DEFAULT_ENTRY_POINT, custom_load_shapes=True, affinity=affinity)

    logging.debug(f"Generated Team config is {test_config}")
    return test_config


def prepare_test_config_with_taint_toleration(tolerations: list[Toleration]) -> TestConfig:
    """
    Create a predictable test configuration.

    Create a `TestConfig` object with taint toleration information
    :param tolerations:
    :return:
    """
    test_config = TestConfig(entry_point=DEFAULT_ENTRY_POINT, custom_load_shapes=True, tolerations=tolerations)

    logging.debug(f"Generated Team config is {test_config}")
    return test_config


def prepare_vanilla_spec_command_seed(team_config: TestConfig) -> str:
    """Prepare a reference vanilla specification."""
    return VANILLA_SPECS_COMMAND_TEMPLATE.format(
        file=_construct_test_file_path(team_config.entry_point),  # type: ignore[arg-type]
        host_url=team_config.vanilla_specs.target_host,  # type: ignore[union-attr]
        users=team_config.vanilla_specs.users,  # type: ignore[union-attr]
        spawn_rate=team_config.vanilla_specs.spawn_rate,  # type: ignore[union-attr]
        run_time=team_config.vanilla_specs.run_time,  # type: ignore[union-attr]
    )


def prepare_custom_load_command_seed(test_config: TestConfig) -> str:
    """Prepare a reference custom load shapes command seed."""
    return CUSTOM_LOAD_SHAPE_COMMAND_TEMPLATE.format(file=_construct_test_file_path(test_config.entry_point))  # type: ignore[arg-type]


def _construct_test_file_path(entry_point: str) -> str:
    return f"{DEFAULT_CONTAINER_TEST_DIR}/{entry_point}"


def prepare_meta_block(name: str, entry_point: str) -> Metadata:
    """Prepare a reference Metadata block."""
    # Operations performed:
    # .split('/')[-1]       >> Split the string on path separator "/" and capture the file name
    # .replace('.py', '')   >> Remove ".py" from the file name
    # .replace("_", "-")    >> Replace any underscore with a '-'
    test_name = entry_point.split("/")[-1].replace(".py", "").replace("_", "-")

    # Detect camel case word boundary start and replace it with a '-'.
    # Examples:
    #   - >AC<amelCase
    test_name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", test_name)

    # Detect camel case word boundary end and replace it with a '-'.
    # Examples:
    #   - ACame>lC<ase
    #   - ACame>l5<Case
    test_name = re.sub(r"([a-z\d])([A-Z])", r"\1-\2", test_name)

    return Metadata(name=f"{name.lower()}.{test_name}")


def prepare_spec_block(test_config: TestConfig) -> Spec:
    """Prepare a reference spec block."""
    cr_config = prepare_reference_cr_configuration(test_config)
    return Spec(
        masterCommandSeed=cr_config.master_command_seed,
        workerCommandSeed=cr_config.worker_command_seed,
        workerReplicas=cr_config.worker_replicas,
        image=cr_config.image,
        configMap=cr_config.config_map,
        labels=cr_config.labels,
        annotations=cr_config.annotations,
        affinity=cr_config.affinity,
        tolerations=cr_config.tolerations,
    )
