from pulumi import automation


def list_stack(project_name: str, runtime: str):
    """returns list of stacks for given workspace in project and runtime"""
    try:
        # select the workspace
        workspace = automation.LocalWorkspace(project_settings=automation.ProjectSettings(name=project_name, runtime=runtime))
        # list the stacks in the workspace
        stacks = workspace.list_stacks()
        return [stack.name for stack in stacks]
    except Exception as exception:
        print(str(exception))
        return []


def read_stack(stack_name: str, project_name: str, output_key: str):
    """reads output value from a specified stack"""
    try:
        # select the stack
        stack = automation.select_stack(stack_name=stack_name,
                                        project_name=project_name,
                                        # no-op program, just to get outputs
                                        program=lambda *args: None)
        outputs = stack.outputs()
        return outputs[output_key].value
    except automation.StackNotFoundError:
        return print(f"stack '{stack_name}' does not exist")
    except Exception as exception:
        print(str(exception))
        return '0'


def create_update_stack(stack_name: str, project_name: str, source_dir: str, cloud_config: dict):
    """creates or updates a stack"""

    try:
        # select the stack or create if does not exist
        stack = automation.create_or_select_stack(stack_name=stack_name,
                                                  project_name=project_name,
                                                  work_dir=source_dir)
        #TODO: support other cloud
        stack.set_config("aws:region", automation.ConfigValue(cloud_config['region']))
        # refresh the stack
        stack.refresh(on_output=print)
        # deploy the stack and output logs to stdout
        stack.up(on_output=print)
        return print(f"stack '{stack_name}' successfully created!")
    except automation.ConcurrentUpdateError:
        return print(f"stack '{stack_name}' already has update in progress")
    except Exception as exception:
        return print(str(exception))


def destroy_stack(stack_name: str, project_name: str):
    """destroys a stack"""
    try:
        # select the stack
        stack = automation.select_stack(stack_name=stack_name,
                                        project_name=project_name,
                                        # noop program for destroy
                                        program=lambda *args: None)
        # refresh the stack
        stack.refresh(on_output=print)
        # destroy the stack and output logs to stdout
        stack.destroy(on_output=print)
        stack.workspace.remove_stack(stack_name)
        return print(f"stack '{stack_name}' successfully removed!")
    except automation.StackNotFoundError:
        return print(f"stack '{stack_name}' does not exist")
    except automation.ConcurrentUpdateError:
        return print(f"stack '{stack_name}' already has update in progress")
    except Exception as exception:
        return print(str(exception))
