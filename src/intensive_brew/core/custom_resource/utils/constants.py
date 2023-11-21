"""Constants for custom resource generation package."""

CUSTOM_LOAD_SHAPE_COMMAND_TEMPLATE = "--locustfile {file}"

VANILLA_SPECS_COMMAND_TEMPLATE = "--locustfile {file} --host {host_url} --users {users} --spawn-rate {spawn_rate} --run-time {run_time} --stop-timeout {termination_timeout}"

# For this iteration, `worker` command template and `custom shapes` command template are identical
WORKER_COMMAND_TEMPLATE = CUSTOM_LOAD_SHAPE_COMMAND_TEMPLATE

DEFAULT_CONTAINER_TEST_DIR = "/lotest/src/"
