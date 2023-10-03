"""the concourse functions and methods for the three primary commands, and their interfacing with the pulumi automation api bindings interface"""  # noqa: E501
import json
import os
import sys
from pathlib import Path

import lib.pulumi


def check_cmd() -> None:
    json.dump([{"id": "0"}], sys.stdout)


def in_cmd() -> None:
    # assign input parameters
    resource_config: dict = __configure_resource()
    # establish optional variables' default values
    if resource_config.get("skip_implicit_get", False):
        payload = {"version": {"id": "0"}}
        json.dump(payload, sys.stdout)
        return
    source_dir: Path = Path(sys.argv[1]).joinpath(
        resource_config.get("source_dir", ".")
    )

    # merge in os env variables
    if "env_os" in resource_config:
        os.environ.update(resource_config["env_os"])

    # read all outputs from stack
    outputs = lib.pulumi.read_stack(
        stack_name=resource_config["stack_name"],
        project_name=resource_config["project_name"],
        source_dir=source_dir,
        env=resource_config,
    )

    # write json formatted outputs to file for later possible use by out
    outputs_path: Path = Path(source_dir).joinpath(
        f"{resource_config['stack_name']}_outputs.json"
    )
    outputs_path.write_text(json.dumps(outputs, indent=2))

    # create payload with stack version and stack outputs metadata
    payload = {"version": {"id": "0"}}
    json.dump(payload, sys.stdout)


def out_cmd() -> None:
    """concourse out command"""  # noqa: D403
    resource_config: dict = __configure_resource()
    refresh_stack: bool = resource_config.get("refresh_stack", True)
    preview: bool = resource_config.get("preview", False)
    source_dir: Path = Path(sys.argv[1]).joinpath(
        resource_config.get("source_dir", ".")
    )
    stack_config: dict = resource_config.get("stack_config", {})
    env_pulumi: dict = resource_config.get("env_pulumi", {})
    version: int = 0
    if "env_os" in resource_config:
        os.environ.update(resource_config["env_os"])

    if resource_config["action"] == "create":
        version = lib.pulumi.create_stack(
            stack_name=resource_config["stack_name"],
            project_name=resource_config["project_name"],
            source_dir=source_dir,
            stack_config=stack_config,
            env=env_pulumi,
            preview=preview,
        )
    elif resource_config["action"] == "update":
        version = lib.pulumi.update_stack(
            stack_name=resource_config["stack_name"],
            project_name=resource_config["project_name"],
            source_dir=source_dir,
            stack_config=stack_config,
            refresh_stack=refresh_stack,
            env=env_pulumi,
            preview=preview,
        )
    elif resource_config["action"] == "destroy":
        version = lib.pulumi.destroy_stack(
            stack_name=resource_config["stack_name"],
            project_name=resource_config["project_name"],
            env=env_pulumi,
            refresh_stack=refresh_stack,
        )
    else:
        raise RuntimeError('Invalid value for "action" parameter')
    json.dump({"version": {"id": str(version)}}, sys.stdout)


def __configure_resource(stream=sys.stdin) -> dict:
    """reads in concourse params and returns efficient params lookup dict"""  # noqa: D401, D403
    inputs: dict = json.load(stream)
    resource_config = {"stack_name": "", "project_name": ""}
    source = inputs.get("source") or {}
    resource_params = inputs.get("params") or {}
    resource_config.update(**source, **resource_params)
    return resource_config
