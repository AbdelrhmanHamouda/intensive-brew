"""Main custom resource generation package."""
import logging as log

from intensive_brew.core.custom_resource.utils.helpers import Helpers
from intensive_brew.core.yaml.validation import Validation


class Generation:
    """Main custom resource generation class."""

    @staticmethod
    def generate(yaml_path: str, output_path: str) -> None:
        """Generate a LocustTest custom resource from a YAML configuration."""
        # Generate internal object mapping
        log.info(f"Collecting raw configuration from file: '{yaml_path}'")

        yaml_configuration = Validation.generate_configuration_object(yaml_path)
        log.debug(f"Parsed YAML config:\n{yaml_configuration}")

        # Generating Custom Resources for collected configuration
        cr_list = Helpers.build_custom_resources(yaml_configuration)

        # Write to the output directory.
        Helpers.write_cr_files(cr_list, output_path)
