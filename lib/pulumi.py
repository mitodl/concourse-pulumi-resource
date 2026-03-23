"""the pulumi CRUD+L interface"""

import sys
from pathlib import Path
from typing import Union

import yaml
from pulumi import automation

from lib.logrus import logger

# Path to the pre-built virtualenv baked into the provisioner Docker image.
# Setting this in the project's Pulumi.yaml causes the uv toolchain to use it
# directly, bypassing searchup() and making `uv sync --inexact` a no-op since
# all packages are already present.
_PREBUILT_VIRTUALENV = "/opt/ol-infrastructure/.venv"


def _inject_virtualenv(source_dir: Union[str, Path]) -> None:
    """Patch the Pulumi.yaml in source_dir to use the pre-built virtualenv.

    Preserves all existing project settings; only adds/overwrites the
    runtime.options.virtualenv key so Pulumi's uv toolchain skips package
    discovery against the ephemeral mounted workspace.
    """
    source_dir = Path(source_dir)
    for ext in (".yaml", ".yml"):
        pulumi_yaml = source_dir / f"Pulumi{ext}"
        if not pulumi_yaml.exists():
            continue
        config = yaml.safe_load(pulumi_yaml.read_text()) or {}
        runtime = config.get("runtime", "python")
        if isinstance(runtime, str):
            runtime = {"name": runtime, "options": {}}
        runtime.setdefault("options", {})
        runtime["options"]["virtualenv"] = _PREBUILT_VIRTUALENV
        config["runtime"] = runtime
        pulumi_yaml.write_text(yaml.dump(config))
        return


def list_stack(project_name: str, runtime: str) -> list:
    """returns list of stacks for given workspace in project and runtime"""  # noqa: D401, D403
    workspace: automation.LocalWorkspace = automation.LocalWorkspace(
        project_settings=automation.ProjectSettings(name=project_name, runtime=runtime)
    )
    stacks: list = workspace.list_stacks()

    return [stack.name for stack in stacks]


def read_stack(
    stack_name: str,
    project_name: str,
    source_dir: Union[str, Path],
    env: dict,
    output_key: str | None = None,
):
    """returns output value or values from a specified stack"""  # noqa: D403, D401
    import sys

    logger.info(sys.argv[1])
    try:
        _inject_virtualenv(source_dir)
        stack: automation.Stack = automation.select_stack(
            stack_name=stack_name,
            project_name=project_name,
            work_dir=source_dir,
            opts=__params_env_to_workspace(params=env),
        )
        outputs: dict = stack.outputs()

        # return single value from outputs, or return all outputs
        if output_key:
            return outputs[output_key].value
        return outputs
    except automation.StackNotFoundError as exception:
        raise automation.StackNotFoundError(
            f"stack '{stack_name}' does not exist"
        ) from exception


def create_stack(  # noqa: PLR0913
    stack_name: str,
    project_name: str,
    source_dir: Union[str, Path],
    stack_config: dict,
    env: dict,
    preview: bool = False,
) -> int:
    """creates a stack and returns its output values"""  # noqa: D403, D401

    logger.info(sys.argv[1])
    try:
        _inject_virtualenv(source_dir)
        # create the stack if it does not exist
        stack: automation.Stack = automation.create_stack(
            stack_name=stack_name,
            project_name=project_name,
            work_dir=source_dir,
            opts=__env_to_workspace(env=env),
        )
        # add config kv pairs
        for config_key, config_value in stack_config.items():
            stack.set_config(config_key, automation.ConfigValue(config_value))
        if preview:
            # preview instead and output to stdout
            logger.info(f"stack '{stack_name}' preview below:")
            stack.preview(on_output=logger.info)
            return 0
        else:
            # deploy the stack and output logs to stdout
            up_result = stack.up(on_output=logger.info)
            logger.info(f"stack '{stack_name}' successfully created!")
            return up_result.summary.version
    except automation.StackAlreadyExistsError as exception:
        raise automation.StackAlreadyExistsError(
            f"stack '{stack_name}' already exists"
        ) from exception


def update_stack(  # noqa: PLR0913
    stack_name: str,
    project_name: str,
    source_dir: Union[str, Path],
    stack_config: dict,
    env: dict | None = None,
    refresh_stack: bool = True,
    preview: bool = False,
    run_program: bool = False,
) -> int:
    """updates a stack and returns its output values"""  # noqa: D403, D401
    import sys

    logger.info(sys.argv[1])
    try:
        _inject_virtualenv(source_dir)
        # updates the stack if not already updating
        stack: automation.Stack = automation.select_stack(
            stack_name=stack_name,
            project_name=project_name,
            work_dir=source_dir,
            opts=__env_to_workspace(env=env),
        )
        # add config kv pairs
        for config_key, config_value in stack_config.items():
            stack.set_config(config_key, automation.ConfigValue(config_value))
        # refresh the stack
        if refresh_stack:
            stack.refresh(on_output=logger.info, run_program=run_program)
        if preview:
            # preview instead and output to stdout
            logger.info(f"stack '{stack_name}' preview below:")
            stack.preview(on_output=logger.info)
            return 0
        else:
            # deploy the stack and output logs to stdout
            up_result = stack.up(on_output=logger.info, run_program=run_program)
            logger.info(f"stack '{stack_name}' successfully updated!")
            return up_result.summary.version
    except automation.ConcurrentUpdateError as exception:
        raise automation.ConcurrentUpdateError(
            f"stack '{stack_name}' already has update in progress"
        ) from exception


def destroy_stack(
    stack_name: str,
    project_name: str,
    env: dict | None = None,
    refresh_stack: bool = False,
    run_program: bool = False,
) -> int:
    """destroys and removes a stack"""  # noqa: D403
    try:
        # select the stack
        stack: automation.Stack = automation.select_stack(
            stack_name=stack_name,
            project_name=project_name,
            # no-op program for destroy
            program=lambda *args: None,
            opts=__env_to_workspace(env=env),
        )
        # refresh the stack
        if refresh_stack:
            stack.refresh(on_output=logger.info, run_program=run_program)
        # destroy the stack and output logs to stdout
        destroy_result = stack.destroy(on_output=logger.info, run_program=run_program)
        stack.workspace.remove_stack(stack_name)
        return destroy_result.summary.version
    except automation.StackNotFoundError as exception:
        raise automation.StackNotFoundError(
            f"stack '{stack_name}' does not exist"
        ) from exception
    except automation.ConcurrentUpdateError as exception:
        raise automation.ConcurrentUpdateError(
            f"stack '{stack_name}' already has update in progress"
        ) from exception
    except Exception as exception:
        raise Exception(str(exception)) from exception


def __env_to_workspace(
    env: dict | None = None,
) -> automation.LocalWorkspaceOptions:
    """converts env dict into workspace options"""  # noqa: D403, D401
    env = env or {}
    aws_shared_credentials_file = Path(sys.argv[1]).joinpath(
        (env).get("AWS_SHARED_CREDENTIALS_FILE", "")
    )
    env["AWS_SHARED_CREDENTIALS_FILE"] = aws_shared_credentials_file
    return automation.LocalWorkspaceOptions(env_vars=env)


def __params_env_to_workspace(
    params: dict,
) -> automation.LocalWorkspaceOptions:
    try:
        env_pulumi = params.get("env_pulumi", {})
        env_os = params.get("env_os", {})
        aws_region = env_os.get("AWS_DEFAULT_REGION", None)
        aws_shared_credentials_file = Path(sys.argv[1]).joinpath(
            env_pulumi.get("AWS_SHARED_CREDENTIALS_FILE", None)
        )
        project_name = params.get("project_name", {})
        s3_bucket = params.get("s3_bucket", "")
    except Exception as e:
        logger.error(e)
        raise e
    else:
        opts = automation.LocalWorkspaceOptions(
            env_vars={
                "AWS_REGION": aws_region,
                "AWS_SHARED_CREDENTIALS_FILE": aws_shared_credentials_file,
            },
            project_settings=automation.ProjectSettings(
                runtime=automation.ProjectRuntimeInfo(name=project_name),
                name=project_name,
                backend=automation.ProjectBackend(url=s3_bucket),
            ),
        )

    return opts
