"""Main validation package."""
import logging as log

import yaml

from intensive_brew.core.dto.configuration import Configuration


class Validation:
    """Main validation class."""

    @staticmethod
    def validate(file_path: str) -> Configuration:
        """Validate a YAML configuration."""
        try:
            # Open configuration file
            with open(file_path) as configuration_file:
                # Safe load yaml
                parsed_yaml = yaml.safe_load(configuration_file)
                log.debug(f"Parsed YAML object:\n{parsed_yaml}")

                # Map object to model
                configuration = Configuration.parse_obj(parsed_yaml)
                log.debug(f"Parsed Configuration:\n{configuration}")

                return configuration
        except Exception as error:
            log.error("Failed to validate YAML configuration.")
            raise error
