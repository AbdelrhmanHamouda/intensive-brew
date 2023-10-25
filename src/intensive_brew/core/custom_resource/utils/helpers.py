"""Main custom resource generation package."""
import logging as log
import pathlib
import re

import yaml

from intensive_brew.core.custom_resource.utils.constants import (
    CUSTOM_LOAD_SHAPE_COMMAND_TEMPLATE,
    DEFAULT_CONTAINER_TEST_DIR,
    VANILLA_SPECS_COMMAND_TEMPLATE,
    WORKER_COMMAND_TEMPLATE,
)
from intensive_brew.core.dto.custom_resource.locust_test_custom_resource import LocustTest
from intensive_brew.core.dto.custom_resource.metadata import Metadata
from intensive_brew.core.dto.custom_resource.spec import Spec
from intensive_brew.core.dto.yaml.configuration import Configuration
from intensive_brew.core.dto.yaml.test_config import TestConfig


class Helpers:
    """Generation helpers class."""

    @staticmethod
    def build_custom_resources(configuration: Configuration) -> list[LocustTest]:
        """
        Build a list of LocustTest objects.

        Generate a list of LocustTest objects based on the passed configuration.
        :param configuration: tests configurations
        :return: List of Custom Resource objects
        """
        log.info("Generating Custom Resources for collected configuration.")

        # Init return list
        cr_list = []

        for test_key, test_config in configuration.configurations.items():
            # Generate `metadata` as defined in the CRD
            resource_metadata = Helpers._generate_cr_metadata(test_key, test_config)

            # Generate resource `spec` block as defined in the CRD
            resource_spec = Helpers._generate_cr_spec(test_config)

            # Generate CR
            custom_resource = LocustTest(metadata=resource_metadata, spec=resource_spec)

            log.info(f"Generated Custom resource for test: {test_key}.")
            log.debug(f"Custom resource: {custom_resource}")

            # Append CR to CR return list
            cr_list.append(custom_resource)

        return cr_list

    @staticmethod
    def _generate_cr_metadata(test_key: str, test_config: TestConfig) -> Metadata:
        """
        Generate a custom resource metadata.

        Method generates a complaint Metadata block based on the requirements of the LocustTest CRD.

        :param test_key: Team name
        :param test_config: Team Configuration
        :return: Metadata object
        """
        # Operations performed:
        # .split('/')[-1]       >> Split the string on path separator "/" and capture the file name
        # .replace('.py', '')   >> Remove ".py" from the file name
        # .replace("_", "-")    >> Replace any underscore with a '-'
        test_name = test_config.entry_point.split("/")[-1].replace(".py", "").replace("_", "-")  # type: ignore[union-attr]

        # Detect camel case word boundary start and replace it with a '-'.
        # Examples:
        #   - >AC<amelCase
        test_name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", test_name)

        # Detect camel case word boundary end and replace it with a '-'.
        # Examples:
        #   - ACame>lC<ase
        #   - ACame>l5<Case
        test_name = re.sub(r"([a-z\d])([A-Z])", r"\1-\2", test_name)

        log.debug(f"Generated test name from the original {test_config.entry_point}, is: {test_name}")

        # Resource name matching CRD required pattern: <teamName>.<testName>
        return Metadata(name=f"{test_key.lower()}.{test_name}")

    @staticmethod
    def _generate_cr_spec(test_config: TestConfig) -> Spec:
        """
        Generate a custom resource spec.

        Method generates a complaint Spec block based on the requirements of the LocustTest CRD.

        :param test_config: Test Configuration
        :return: Spec object
        """
        # Image
        image = test_config.image

        # Generate locust command seeds
        master_command_seed = Helpers._generate_master_command_seed(test_config)
        worker_command_seed = Helpers._generate_worker_command_seed(test_config)

        # Workers replica count
        worker_replicas = test_config.worker_replicas

        # Config map
        config_map = test_config.configmap

        # Labels
        labels = test_config.labels

        # Annotations
        annotations = test_config.annotations

        # Affinity
        affinity = test_config.affinity

        # Taint tolerations
        tolerations = test_config.tolerations

        return Spec(
            image=image,  # type: ignore[arg-type]
            masterCommandSeed=master_command_seed,
            workerCommandSeed=worker_command_seed,
            workerReplicas=worker_replicas,  # type: ignore[arg-type]
            configMap=config_map,
            annotations=annotations,
            labels=labels,
            affinity=affinity,
            tolerations=tolerations,
        )

    @staticmethod
    def _generate_master_command_seed(test_config: TestConfig) -> str:
        """
        Generate a master node command seed.

        Method to Generate 'MASTER' node command seed based on test configuration.
        :param test_config:
        :return:
        """
        # Expert mode
        if Helpers._is_expert(test_config):
            command = test_config.expert_mode.masterCommandSeed  # type: ignore[union-attr]

        # Custom load shapes
        elif not Helpers._is_expert(test_config) and test_config.custom_load_shapes:
            command = CUSTOM_LOAD_SHAPE_COMMAND_TEMPLATE.format(file=Helpers._construct_test_file_path(test_config.entry_point))  # type: ignore[arg-type]

        # Vanilla Specs
        else:
            command = VANILLA_SPECS_COMMAND_TEMPLATE.format(
                file=Helpers._construct_test_file_path(test_config.entry_point),  # type: ignore[arg-type]
                host_url=test_config.vanilla_specs.target_host,  # type: ignore[union-attr]
                users=test_config.vanilla_specs.users,  # type: ignore[union-attr]
                spawn_rate=test_config.vanilla_specs.spawn_rate,  # type: ignore[union-attr]
                run_time=test_config.vanilla_specs.run_time,  # type: ignore[union-attr]
                stop_timeout=test_config.vanilla_specs.stop_timeout,  # type: ignore[union-attr]
            )

        log.debug(f"Generated 'MASTER' node command seed: {command}")
        return command

    @staticmethod
    def _is_expert(test_config: TestConfig) -> bool:
        """Check for expert mode."""
        # Since `expert_mode` is an optional field, not all configurations will have it
        # + thus the conditional is checking if object exists and if it does, it is enabled
        return True if (test_config.expert_mode and test_config.expert_mode.enabled) else False

    @staticmethod
    def _construct_test_file_path(entry_point: str) -> str:
        file_path = f"{DEFAULT_CONTAINER_TEST_DIR}/{entry_point}"
        log.debug(f"Constructed file path : {file_path}")

        return file_path

    @staticmethod
    def _generate_worker_command_seed(test_config: TestConfig) -> str:
        """
        Generate a worker node command seed.

        Method to Generate 'WORKER' node command seed based on team configuration.
        :param test_config:
        :return:
        """
        # Expert mode
        if Helpers._is_expert(test_config):
            command_seed = test_config.expert_mode.workerCommandSeed  # type: ignore[union-attr]

        # Default mode
        else:
            command_seed = WORKER_COMMAND_TEMPLATE.format(file=Helpers._construct_test_file_path(test_config.entry_point))  # type: ignore[arg-type]

        log.debug(f"Generated 'WORKER' node command seed: {command_seed}")
        return command_seed

    @staticmethod
    def write_cr_files(cr_list: list[LocustTest], output_dir: str) -> None:
        """Write a collection of yaml files to the desired output directory."""
        # Create output directory if it doesn't exist
        Helpers._check_or_create_output_dir(output_dir)

        # Loop over the provided custom resource list
        for custom_resource in cr_list:
            complete_file_path = f"{output_dir}/{custom_resource.metadata.name}.yaml"
            config = yaml.dump(custom_resource.dict(by_alias=True, exclude_none=True))
            log.info(f"Writing configuration for test:{custom_resource.metadata.name} at {complete_file_path}.")
            log.debug(f"Configuration \n{config}")

            # Write to CR file
            with open(complete_file_path, "w") as cr_file:
                # Writing data to a file
                cr_file.write(config)

    @staticmethod
    def _check_or_create_output_dir(output_dir: str) -> None:
        """Create output directory if it doesn't exist."""
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
