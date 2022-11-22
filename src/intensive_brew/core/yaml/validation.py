"""Main validation package."""
import logging as log

import yaml

from intensive_brew.core.dto.yaml.configuration import Configuration


class Validation:
    """Main validation class."""

    @staticmethod
    def generate_configuration_object(file_path: str) -> Configuration:
        """Generate a mapped Configuration object."""
        # Open configuration file
        with open(file_path) as configuration_file:
            # Safe load yaml
            parsed_yaml = yaml.safe_load(configuration_file)
            log.debug(f"Parsed YAML object:\n{parsed_yaml}")

        # Map object to model
        return Configuration.parse_obj(parsed_yaml)

    @staticmethod
    def validate(file_path: str) -> Configuration:
        """Validate a YAML configuration."""
        try:
            configuration = Validation.generate_configuration_object(file_path)
            log.debug(f"Parsed Configuration:\n{configuration}")

            return configuration
        except Exception as error:
            log.error("Failed to validate YAML configuration.")
            raise error
