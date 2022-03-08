"""the concourse functions and methods for the three primary commands, and their interfacing with the pulumi automation api bindings interface"""
import json
import logging
import os
import pathlib
import sys

import lib.pulumi

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger(__name__)


def check_cmd() -> None:
    json.dump({"id": 0}, sys.stdout)


def in_cmd() -> None:
    # assign input parameters
    params: dict = __read_params()
    # establish optional variables' default values
    source_dir: str = __pulumi_source_dir(
        "/tmp/build/put", params.get("source_dir", ".")
    )
    env_pulumi: dict = params.get("env_pulumi", {})

    # merge in os env variables
    if "env_os" in params:
        os.environ.update(params["env_os"])

    # read all outputs from stack
    outputs: dict = lib.pulumi.read_stack(
        stack_name=params["stack_name"],
        project_name=params["project_name"],
        source_dir=source_dir,
        env=env_pulumi,
    )

    # write json formatted outputs to file for later possible use by out
    outputs_path: str = str(
        pathlib.Path(source_dir).joinpath(f"{params['stack_name']}_outputs.json")
    )
    with open(outputs_path, "w", encoding="utf8") as json_file:
        # output dictionary as json to file
        json_file.write(json.dumps(outputs, indent=2))

    # create payload with stack version and stack outputs metadata
    payload: dict = {
        "version": {"id": 0},
        "metadata": {params["stack_name"]: outputs},
    }

    json.dump(payload, sys.stdout)


def out_cmd() -> None:
    """concourse out command"""
    params: dict = __read_params()
    refresh_stack: bool = params.get("refresh_stack", True)
    preview: bool = params.get("preview", False)
    source_dir: str = __pulumi_source_dir(
        "/tmp/build/put", params.get("source_dir", ".")
    )
    stack_config: dict = params.get("stack_config", {})
    env_pulumi: dict = params.get("env_pulumi", {})
    outputs: dict = {"version": ""}
    if "env_os" in params:
        os.environ.update(params["env_os"])

    if params["action"] == "create":
        outputs = lib.pulumi.create_stack(
            stack_name=params["stack_name"],
            project_name=params["project_name"],
            source_dir=source_dir,
            stack_config=stack_config,
            env=env_pulumi,
            preview=preview,
        )
    elif params["action"] == "update":
        outputs = lib.pulumi.update_stack(
            stack_name=params["stack_name"],
            project_name=params["project_name"],
            source_dir=source_dir,
            stack_config=stack_config,
            refresh_stack=refresh_stack,
            env=env_pulumi,
            preview=preview,
        )
    elif params["action"] == "destroy":
        lib.pulumi.destroy_stack(
            stack_name=params["stack_name"],
            project_name=params["project_name"],
            env=env_pulumi,
            refresh_stack=refresh_stack,
        )
    else:
        raise RuntimeError('Invalid value for "action" parameter')
    json.dump({"version": {"id": 0}}, sys.stdout)


def __read_params(stream=sys.stdin) -> dict:
    """reads in concourse params and returns efficient params lookup dict"""
    inputs: dict = json.load(stream)
    return inputs.get("params", {"stack_name": "", "project_name": ""})


def __pulumi_source_dir(prefix_path: str, param_source_dir: str):
    """determines path to pulumi source dir and returns as str for automation api input"""
    return str(pathlib.Path(prefix_path).joinpath(param_source_dir))
