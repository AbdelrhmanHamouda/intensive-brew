"""Utils package for dtos."""


def is_expert(values_dict: dict) -> bool:  # type: ignore[type-arg]
    """Validate if 'expert_mode' is being used in the configuration."""
    return True if (values_dict["expert_mode"] and values_dict["expert_mode"].enabled) else False
