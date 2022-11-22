"""Validation test module."""
import pytest
from pydantic import ValidationError

from intensive_brew.core.dto.expert_mode import ExpertMode
from intensive_brew.core.dto.test_config import TestConfig
from intensive_brew.core.dto.vanilla_specs import VanillaSpecs


def test_vanilla_specs() -> None:
    """Check creating an object with bare-minimum configuration for vanilla_specs."""
    assert TestConfig(
        entry_point="my_script.py",
        vanilla_specs=VanillaSpecs(
            users=1000,
            spawn_rate=10,
            run_time="60s",
            target_host="http://localhost:8080",  # type: ignore[arg-type]
        ),
    )


def test_custom_load_shap() -> None:
    """Check creating an object with bare-minimum configuration for custom_load_shap."""
    assert TestConfig(entry_point="my_script.py", custom_load_shapes=True)


def test_expert_mode() -> None:
    """Check creating an object with bare-minimum configuration for expert_mode."""
    assert TestConfig(expert_mode=ExpertMode(enabled=True, masterCommandSeed="Master command", workerCommandSeed="Worker command"))


def test_validation_for_entry_point_with_expert_missing() -> None:
    """Check when expert mode is not mentioned, entry point is needed."""
    with pytest.raises(ValidationError):
        assert TestConfig(entry_point=None)


def test_validation_for_entry_point_with_expert_false() -> None:
    """Check when expert mode is False, entry point is needed."""
    with pytest.raises(ValidationError):
        assert TestConfig(
            expert_mode=ExpertMode(enabled=False, masterCommandSeed="Master command", workerCommandSeed="Worker command"),
            entry_point=None,
        )


def test_validation_for_vanilla_specs_with_expert_false() -> None:
    """Check when expert mode is False, vanilla specs are needed."""
    with pytest.raises(ValidationError):
        assert TestConfig(
            expert_mode=ExpertMode(enabled=False, masterCommandSeed="Master command", workerCommandSeed="Worker command"),
            entry_point="my_script.py",
            vanilla_specs=None,
        )


def test_validation_for_vanilla_specs_with_custom_load_shap_false() -> None:
    """Check when custom load shap mode is False, vanilla specs are needed."""
    with pytest.raises(ValidationError):
        assert TestConfig(entry_point="my_script.py", custom_load_shapes=False, vanilla_specs=None)


def test_target_host_websocket_url_validation() -> None:
    """Check that providing a websocket as a target host is accepted."""
    assert TestConfig(
        entry_point="my_script.py",
        vanilla_specs=VanillaSpecs(
            users=1000,
            spawn_rate=10,
            run_time="60s",
            target_host="ws://endpoint.data.eu.dev.cloud:8080",  # type: ignore[arg-type]
        ),
    )


def test_run_time_validation_with_long_value() -> None:
    """Check that passing a valid long form run_time doesn't rais error."""
    assert TestConfig(
        entry_point="my_script.py",
        vanilla_specs=VanillaSpecs(
            users=1000,
            spawn_rate=10,
            run_time="44h44m60s",
            target_host="http://localhost:8080",  # type: ignore[arg-type]
        ),
    )


def test_run_time_validation_with_invalid_value() -> None:
    """Check that passing an invalid  run_time raises an error."""
    with pytest.raises(ValidationError):
        assert TestConfig(
            entry_point="my_script.py",
            vanilla_specs=VanillaSpecs(
                users=1000,
                spawn_rate=10,
                run_time="44hw",
                target_host="http://localhost:8080",  # type: ignore[arg-type]
            ),
        )


def test_run_time_validation_with_complex_invalid_value() -> None:
    """Check that passing an invalid  run_time raises an error."""
    with pytest.raises(ValidationError):
        assert TestConfig(
            entry_point="my_script.py",
            vanilla_specs=VanillaSpecs(
                users=1000,
                spawn_rate=10,
                run_time="1h30w5s",
                target_host="http://localhost:8080",  # type: ignore[arg-type]
            ),
        )
