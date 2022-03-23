"""the concourse functions and methods for the three primary commands, and their interfacing with the pulumi automation api bindings interface"""
import json
import os
import pathlib
import sys

import lib.pulumi
from lib.logrus import logger


def check_cmd() -> None:
    json.dump([{"id": "0"}], sys.stdout)


def in_cmd() -> None:
    # assign input parameters
    params: dict = __read_params()
    logger.info(json.dumps(params))
    # establish optional variables' default values
    source_dir: str = sys.argv[1] + "/" + params.get("source_dir", ".")

    # merge in os env variables
    if "env_os" in params:
        os.environ.update(params["env_os"])

    # read all outputs from stack
    outputs = lib.pulumi.read_stack(
        stack_name=params["stack_name"],
        project_name=params["project_name"],
        source_dir=source_dir,
        env=params,
    )

    # write json formatted outputs to file for later possible use by out
    outputs_path: str = str(
        pathlib.Path(source_dir).joinpath(f"{params['stack_name']}_outputs.json")
    )
    with open(outputs_path, "w", encoding="utf8") as json_file:
        # output dictionary as json to file
        json_file.write(json.dumps(outputs, indent=2))

    # create payload with stack version and stack outputs metadata
    payload = {"version": {"id": "0"}}
    json.dump(payload, sys.stdout)


def out_cmd() -> None:
    """concourse out command"""
    params: dict = __read_params()
    refresh_stack: bool = params.get("refresh_stack", True)
    preview: bool = params.get("preview", False)
    source_dir: str = sys.argv[1] + "/" + params.get("source_dir", ".")
    stack_config: dict = params.get("stack_config", {})
    env_pulumi: dict = params.get("env_pulumi", {})
    version: int = 0
    if "env_os" in params:
        os.environ.update(params["env_os"])

    if params["action"] == "create":
        version = lib.pulumi.create_stack(
            stack_name=params["stack_name"],
            project_name=params["project_name"],
            source_dir=source_dir,
            stack_config=stack_config,
            env=env_pulumi,
            preview=preview,
        )
    elif params["action"] == "update":
        version = lib.pulumi.update_stack(
            stack_name=params["stack_name"],
            project_name=params["project_name"],
            source_dir=source_dir,
            stack_config=stack_config,
            refresh_stack=refresh_stack,
            env=env_pulumi,
            preview=preview,
        )
    elif params["action"] == "destroy":
        version = lib.pulumi.destroy_stack(
            stack_name=params["stack_name"],
            project_name=params["project_name"],
            env=env_pulumi,
            refresh_stack=refresh_stack,
        )
    else:
        raise RuntimeError('Invalid value for "action" parameter')
    json.dump({"version": {"id": str(version)}}, sys.stdout)


def __read_params(stream=sys.stdin) -> dict:
    """reads in concourse params and returns efficient params lookup dict"""
    inputs: dict = json.load(stream)
    return inputs.get("params", {"stack_name": "", "project_name": ""})
