"""Test package."""
from intensive_brew.core.custom_resource.utils.constants import WORKER_COMMAND_TEMPLATE
from intensive_brew.core.custom_resource.utils.helpers import Helpers
from tests.generation.fixtures import (
    DEFAULT_EXPERT_MODE_SEED_CMD,
    _construct_test_file_path,
    prepare_custom_load_command_seed,
    prepare_test_config,
    prepare_vanilla_spec_command_seed,
)


def test_master_command_seed_generation_with_expert_mode() -> None:
    """Check the functionality of generating command seeds for a `master` node with expert mode enabled."""
    # * Setup
    test_config = prepare_test_config(mode="expert")

    # * Act
    master_node_command_seed = Helpers._generate_master_command_seed(test_config)

    # * Assert
    assert master_node_command_seed == DEFAULT_EXPERT_MODE_SEED_CMD


def test_master_command_seed_generation_with_custom_load_shapes() -> None:
    """Check the functionality of generating command seeds for a `master` node with custom load shapes."""
    # * Setup
    test_config = prepare_test_config(mode="custom")
    expected_command_seed = prepare_custom_load_command_seed(test_config)

    # * Act
    master_node_command_seed = Helpers._generate_master_command_seed(test_config)

    # * Assert
    assert master_node_command_seed == expected_command_seed


def test_master_command_seed_generation_with_vanilla_specs() -> None:
    """Check the functionality of generating command seeds for a `master` node with vanilla specs."""
    # * Setup
    test_config = prepare_test_config(mode="vanilla")
    expected_command_seed = prepare_vanilla_spec_command_seed(test_config)

    # * Act
    master_node_command_seed = Helpers._generate_master_command_seed(test_config)

    # * Assert
    assert master_node_command_seed == expected_command_seed


def test_worker_command_seed_generation_with_expert_mode() -> None:
    """Check the functionality of generating command seeds for a `worker` node with expert mode enabled."""
    # * Setup
    test_config = prepare_test_config(mode="expert")

    # * Act
    worker_node_command_seed = Helpers._generate_worker_command_seed(test_config)

    # * Assert
    assert worker_node_command_seed == DEFAULT_EXPERT_MODE_SEED_CMD


def test_worker_command_seed_generation_with_vanilla_specs() -> None:
    """Check the functionality of generating command seeds for a `worker` node with vanilla specs."""
    # * Setup
    test_config = prepare_test_config(mode="vanilla")
    expected_command_seed = WORKER_COMMAND_TEMPLATE.format(
        file=_construct_test_file_path(test_config.entry_point)  # type: ignore[arg-type]
    )

    # * Act
    worker_node_command_seed = Helpers._generate_worker_command_seed(test_config)

    # * Assert
    assert worker_node_command_seed == expected_command_seed
