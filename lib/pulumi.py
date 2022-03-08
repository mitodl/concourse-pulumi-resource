"""the pulumi CRUD+L interface"""
import logging
import sys

from pulumi import automation

logging.basicConfig(stream=sys.stderr)
log = logging.getLogger(__name__)

logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)
fileHandler = logging.FileHandler("/var/log/pulumi.log")
fileHandler.setFormatter(logFormatter)

log.addHandler(fileHandler)


def list_stack(project_name: str, runtime: str) -> list:
    """returns list of stacks for given workspace in project and runtime"""
    # select the workspace
    workspace: automation._local_workspace.LocalWorkspace = automation.LocalWorkspace(
        project_settings=automation.ProjectSettings(name=project_name, runtime=runtime)
    )
    # list the stacks in the workspace
    stacks: list = workspace.list_stacks()

    return [stack.name for stack in stacks]


def read_stack(
    stack_name: str,
    project_name: str,
    source_dir: str,
    env: dict = None,
    output_key: str = None,
):
    """returns output value or values from a specified stack"""
    try:
        # select the stack
        stack: automation._stack.Stack = automation.select_stack(
            stack_name=stack_name,
            project_name=project_name,
            work_dir=source_dir,
            opts=__env_to_workspace(env=env),
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


def create_stack(
    stack_name: str,
    project_name: str,
    source_dir: str,
    stack_config: dict,
    env: dict = None,
    preview: bool = False,
) -> dict:
    """creates a stack and returns its output values"""

    try:
        # create the stack if it does not exist
        stack: automation._stack.Stack = automation.create_stack(
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
            log.info(f"stack '{stack_name}' preview below:")
            stack.preview(on_output=log.info)
        else:
            # deploy the stack and output logs to stdout
            stack.up(on_output=log.info)
            log.info(f"stack '{stack_name}' successfully created!")

        # return stack outputs
        return stack.outputs()
    except automation.StackAlreadyExistsError as exception:
        raise automation.StackAlreadyExistsError(
            f"stack '{stack_name}' already exists"
        ) from exception


def update_stack(
    stack_name: str,
    project_name: str,
    source_dir: str,
    stack_config: dict,
    env: dict = None,
    refresh_stack: bool = True,
    preview: bool = False,
) -> dict:
    """updates a stack and returns its output values"""

    try:
        # updates the stack if not already updating
        stack: automation._stack.Stack = automation.select_stack(
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
            stack.refresh(on_output=log.info)
        if preview:
            # preview instead and output to stdout
            log.info(f"stack '{stack_name}' preview below:")
            stack.preview(on_output=log.info)
        else:
            # deploy the stack and output logs to stdout
            stack.up(on_output=log.info)
            log.info(f"stack '{stack_name}' successfully updated!")

        # return stack outputs
        stack_outputs = stack.outputs()
        log.info("Stack outputs after update.", stack_outputs)
        return stack_outputs
    except automation.ConcurrentUpdateError as exception:
        raise automation.ConcurrentUpdateError(
            f"stack '{stack_name}' already has update in progress"
        ) from exception


def destroy_stack(
    stack_name: str, project_name: str, env: dict = None, refresh_stack: bool = False
) -> None:
    """destroys and removes a stack"""
    try:
        # select the stack
        stack: automation._stack.Stack = automation.select_stack(
            stack_name=stack_name,
            project_name=project_name,
            # no-op program for destroy
            program=lambda *args: None,
            opts=__env_to_workspace(env=env),
        )
        # refresh the stack
        if refresh_stack:
            stack.refresh(on_output=log.info)
        # destroy the stack and output logs to stdout
        stack.destroy(on_output=log.info)
        stack.workspace.remove_stack(stack_name)

        return f"stack '{stack_name}' successfully destroyed and  removed!"
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


def __env_to_workspace(env: dict) -> automation._local_workspace.LocalWorkspaceOptions:
    """converts env dict into workspace options"""
    return automation.LocalWorkspaceOptions(env_vars=env)
