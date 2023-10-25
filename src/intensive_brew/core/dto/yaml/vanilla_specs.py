"""DTO package."""
import re

from pydantic import AnyUrl, BaseModel, validator


class VanillaSpecs(BaseModel):
    """Base specs for test."""

    class Config:
        """Pydantic config inner class."""

        allow_mutation = False

    # * Number if users
    users: int

    # * Users spawn rate
    spawn_rate: int

    # * Test duration: Stop after the specified amount of time, e.g. (300s, 20m, 3h, 1h30m, etc.). Default: 30s.
    run_time: str = "30s"

    # * Number of seconds to wait for a simulated user to complete any executing task before exiting. Default: 0.
    stop_timeout: int = 0

    # * Target URL of the test
    target_host: AnyUrl

    @validator("run_time")
    def check_run_time(cls, param_value):  # type: ignore[no-untyped-def] # noqa: N805
        """Validate compatible run time."""
        valid_test_duration = ["s", "m", "h"]
        # Matches duration patter e.g. (4h50m15s)
        # Each (number value + time unit) combination is considered a match
        # Inside each match:
        # Group 1 - index 0: complete combination e.g. 4h, 50m, 15s
        # Group 2 - index 1: number value e.g. 4, 50, 15
        # Group 3 - index 2: time unit e.g. h, m, s
        pattern = r"((\d+)([a-zA-Z]+))"
        regex = re.compile(pattern)
        if regex.match(param_value):
            regex_matches = regex.findall(param_value)
            for match in regex_matches:
                if not match[2] in valid_test_duration:
                    raise ValueError(
                        f"The time unit for test duration must be a valid value e.g.({valid_test_duration}). Provided value: {param_value}"
                    )
        else:
            raise ValueError(
                f"The field 'run_time' must be populated with a valid duration, e.g. (300s, 20m, 3h, 1h30m, etc..). Provided value: {param_value}"
            )

        return param_value
