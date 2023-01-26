"""Test package."""

import logging as log
import shutil
from pathlib import Path

import pytest

from intensive_brew.core.custom_resource.utils.helpers import Helpers
from intensive_brew.core.dto.custom_resource.toleration import Toleration
from intensive_brew.core.dto.yaml.configuration import Configuration
from tests.generation.fixtures import (
    DEFAULT_ENTRY_POINT,
    prepare_meta_block,
    prepare_spec_block,
    prepare_test_config,
    prepare_test_config_with_node_affinity,
    prepare_test_config_with_taint_toleration,
)

DEFAULT_NX_PERF_ITG_API_VERSION = "locust.io/v1"
DEFAULT_NX_PERF_ITG_KIND = "LocustTest"


@pytest.fixture()
def dir_cleanup():  # type: ignore[no-untyped-def]
    """Cleanup fixture."""
    created_dirs = []  # type: ignore[var-annotated]
    yield created_dirs
    log.debug("Output directory cleanup...")
    [shutil.rmtree(directory) for directory in created_dirs]  # type: ignore[func-returns-value]


def test_cr_metadata_generation() -> None:
    """Check logic for generating `metadata` block for the Custom Resource is compliant with CRD."""
    # * Setup
    test_key = "loadTest"
    test_config = prepare_test_config("custom")
    expected_meta_block = prepare_meta_block(test_key, DEFAULT_ENTRY_POINT)

    # * Act
    meta_block = Helpers._generate_cr_metadata(test_key, test_config)

    # * Assert
    assert meta_block == expected_meta_block


def test_cr_spec_generation() -> None:
    """Check logic for generating `spec` block for the Custom Resource is compliant with CRD."""
    # * Setup
    test_config = prepare_test_config("expert")
    expected_spec_block = prepare_spec_block(test_config)

    # * Act
    spec_block = Helpers._generate_cr_spec(test_config)

    # * Assert
    assert spec_block == expected_spec_block


def test_cr_spec_generation_with_node_affinity() -> None:
    """Check logic for generating `spec` block with Node Affinity for the Custom Resource is compliant with CRD."""
    # * Setup
    affinity_map = {"nodeGroup-label": "dedicated-performance"}
    test_config = prepare_test_config_with_node_affinity(affinity_map)
    expected_spec_block = prepare_spec_block(test_config)

    # * Act
    spec_block = Helpers._generate_cr_spec(test_config)

    # * Assert
    assert spec_block == expected_spec_block


def test_cr_spec_generation_with_taint_toleration() -> None:
    """Check logic for generating `spec` block with Taint tolerations for the Custom Resource is compliant with CRD."""
    # * Setup
    toleration_a = Toleration(key="hardware", operator="Equal", effect="NoSchedule", value="ssd")
    toleration_b = Toleration(key="dedicated", operator="Exists", effect="NoSchedule")
    test_config = prepare_test_config_with_taint_toleration([toleration_a, toleration_b])
    expected_spec_block = prepare_spec_block(test_config)

    # * Act
    spec_block = Helpers._generate_cr_spec(test_config)

    # * Assert
    assert spec_block == expected_spec_block


def test_cr_object_generation() -> None:
    """Check logic for generating complete `Custom Resource` for the Custom Resource is compliant with CRD."""
    # * Setup
    test_key = "TLM"
    test_config = prepare_test_config("vanilla")
    expected_meta_block = prepare_meta_block(test_key, DEFAULT_ENTRY_POINT)
    expected_spec_block = prepare_spec_block(test_config)
    api_version = DEFAULT_NX_PERF_ITG_API_VERSION
    kind = DEFAULT_NX_PERF_ITG_KIND

    # * Act
    custom_resource_list = Helpers.build_custom_resources(Configuration(configurations={test_key: test_config}))
    custom_resource = custom_resource_list.pop(0)

    # * Assert
    assert custom_resource.api_version == api_version
    assert custom_resource.kind == kind
    assert custom_resource.metadata == expected_meta_block
    assert custom_resource.spec == expected_spec_block


def test_cr_file_generation(dir_cleanup) -> None:  # type: ignore[no-untyped-def]
    """Check that writing into file works as expected."""
    # * Setup
    test_key = "TLM"
    test_config = prepare_test_config("vanilla")
    custom_resource_list = Helpers.build_custom_resources(Configuration(configurations={test_key: test_config}))
    # Output directory and file name
    out_directory = "./test-outs"
    directory_path = Path(out_directory)
    file_path = Path(f"{out_directory}/{custom_resource_list[0].metadata.name}.yaml")

    # * Act
    # Add output directory to clean-up list
    dir_cleanup.append(directory_path.absolute())
    Helpers.write_cr_files(custom_resource_list, out_directory)

    # * Assert
    assert directory_path.is_dir()  # Check directory got created
    assert file_path.is_file()  # check file got created
