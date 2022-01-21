"""the pulumi CRUD+L interface"""
from pulumi import automation


def list_stack(project_name: str, runtime: str) -> list:
    """returns list of stacks for given workspace in project and runtime"""
    try:
        # select the workspace
        workspace = automation.LocalWorkspace(project_settings=automation.ProjectSettings(name=project_name, runtime=runtime))
        # list the stacks in the workspace
        stacks = workspace.list_stacks()

        return [stack.name for stack in stacks]
    except Exception as exception:
        raise Exception(str(exception)) from exception


def read_stack(stack_name: str, project_name: str, output_key: str = None):
    """returns output value or values from a specified stack"""
    try:
        # select the stack
        stack = automation.select_stack(stack_name=stack_name,
                                        project_name=project_name,
                                        # no-op program, just to get outputs
                                        program=lambda *args: None)
        outputs = stack.outputs()

        # return single value from outputs, or return all outputs
        if output_key:
            return outputs[output_key].value
        return outputs
    except automation.StackNotFoundError as exception:
        raise automation.StackNotFoundError(f"stack '{stack_name}' does not exist") from exception
    except Exception as exception:
        raise Exception(str(exception)) from exception


def create_stack(
    stack_name: str,
    project_name: str,
    source_dir: str,
    stack_config: dict,
    preview: bool = False
) -> dict:
    """creates a stack and returns its output values"""

    try:
        # create the stack if it does not exist
        stack = automation.create_stack(stack_name=stack_name,
                                        project_name=project_name,
                                        work_dir=source_dir)
        # add config kv pairs
        for config_key, config_value in stack_config.items():
            stack.set_config(config_key, automation.ConfigValue(config_value))
        if preview:
            # preview instead and output to stdout
            print(f"stack '{stack_name}' preview below:")
            stack.preview(on_output=print)
        else:
            # deploy the stack and output logs to stdout
            stack.up(on_output=print)
            print(f"stack '{stack_name}' successfully created!")

        # return stack outputs
        return stack.outputs()
    except automation.StackAlreadyExistsError as exception:
        raise automation.StackAlreadyExistsError(f"stack '{stack_name}' already exists") from exception
    except Exception as exception:
        raise Exception(str(exception)) from exception


def update_stack(
    stack_name: str,
    project_name: str,
    source_dir: str,
    stack_config: dict,
    refresh_stack: bool = True,
    preview: bool = False
) -> dict:
    """updates a stack and returns its output values"""

    try:
        # updates the stack if not already updating
        stack = automation.select_stack(stack_name=stack_name,
                                        project_name=project_name,
                                        work_dir=source_dir)
        # add config kv pairs
        for config_key, config_value in stack_config.items():
            stack.set_config(config_key, automation.ConfigValue(config_value))
        # refresh the stack
        if refresh_stack:
            stack.refresh(on_output=print)
        if preview:
            # preview instead and output to stdout
            print(f"stack '{stack_name}' preview below:")
            stack.preview(on_output=print)
        else:
            # deploy the stack and output logs to stdout
            stack.up(on_output=print)
            print(f"stack '{stack_name}' successfully updated!")

        # return stack outputs
        return stack.outputs()
    except automation.ConcurrentUpdateError as exception:
        raise automation.ConcurrentUpdateError(f"stack '{stack_name}' already has update in progress") from exception
    except Exception as exception:
        raise Exception(str(exception)) from exception


def destroy_stack(stack_name: str, project_name: str, refresh_stack: bool = False) -> None:
    """destroys and removes a stack"""
    try:
        # select the stack
        stack = automation.select_stack(stack_name=stack_name,
                                        project_name=project_name,
                                        # no-op program for destroy
                                        program=lambda *args: None)
        # refresh the stack
        if refresh_stack:
            stack.refresh(on_output=print)
        # destroy the stack and output logs to stdout
        stack.destroy(on_output=print)
        stack.workspace.remove_stack(stack_name)

        return print(f"stack '{stack_name}' successfully destroyed and  removed!")
    except automation.StackNotFoundError as exception:
        raise automation.StackNotFoundError(f"stack '{stack_name}' does not exist") from exception
    except automation.ConcurrentUpdateError as exception:
        raise automation.ConcurrentUpdateError(f"stack '{stack_name}' already has update in progress") from exception
    except Exception as exception:
        raise Exception(str(exception)) from exception
