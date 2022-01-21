"""the concourse functions and methods for the three primary commands, and their interfacing with the pulumi automation api bindings interface"""
import json
import pathlib
import sys

import lib.pulumi


def check_cmd() -> str:
    """concourse check command"""
    # assign input parameters
    params: dict = __read_params()
    # establish optional variables' default values
    source_dir: str = __pulumi_source_dir(params.get("source_dir", "."))

    # read version value from stack
    version: str = lib.pulumi.read_stack(
        stack_name=params["stack_name"],
        project_name=params["project_name"],
        source_dir=source_dir,
        output_key="version",
    )

    # dump out json payload
    return json.dump({"version": version}, sys.stdout)


def in_cmd() -> str:
    """concourse in command"""
    # assign input parameters
    params: dict = __read_params()
    # establish optional variables' default values
    source_dir: str = __pulumi_source_dir(params.get("source_dir", "."))
    # read all outputs from stack
    outputs: dict = lib.pulumi.read_stack(
        stack_name=params["stack_name"],
        project_name=params["project_name"],
        source_dir=source_dir,
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
        "version": outputs["version"].value,
        "metadata": {params["stack_name"]: outputs},
    }

    return json.dump(payload, sys.stdout)


def out_cmd() -> str:
    """concourse out command"""
    # assign input parameters
    params: dict = __read_params()
    # establish optional variables' default values
    refresh_stack: bool = params.get("refresh_stack", True)
    preview: bool = params.get("preview", False)
    source_dir: str = __pulumi_source_dir(params.get("source_dir", "."))
    stack_config: dict = params.get("stack_config", {})
    # initialize outputs
    outputs: dict = {"version": ""}

    # create pulumi stack
    if params["action"] == "create":
        outputs: dict = lib.pulumi.create_stack(
            stack_name=params["stack_name"],
            project_name=params["project_name"],
            source_dir=str(source_dir),
            stack_config=stack_config,
            preview=preview,
        )
    # update pulumi stack
    elif params["action"] == "update":
        outputs: dict = lib.pulumi.update_stack(
            stack_name=params["stack_name"],
            project_name=params["project_name"],
            source_dir=str(source_dir),
            stack_config=stack_config,
            refresh_stack=refresh_stack,
            preview=preview,
        )
    # destroy pulumi stack
    elif params["action"] == "destroy":
        lib.pulumi.destroy_stack(
            stack_name=params["stack_name"],
            project_name=params["project_name"],
            refresh_stack=refresh_stack,
        )
    else:
        raise RuntimeError('Invalid value for "action" parameter')
    # dump out json payload
    return json.dump({"version": outputs["version"].value}, sys.stdout)


def __read_params(stream=sys.stdin) -> dict:
    """reads in concourse params and returns efficient params lookup dict"""
    inputs: dict = json.load(stream)
    return inputs["params"]


def __pulumi_source_dir(param_source_dir: str):
    """determines path to pulumi source dir and returns as str for automation api input"""
    return str(pathlib.Path(sys.argv[1]).joinpath(param_source_dir))
