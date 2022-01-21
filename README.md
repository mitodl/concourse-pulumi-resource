# Concourse Pulumi Resource

A [concourse-ci](https://concourse-ci.org) resource for provisioning infrastructure via [Pulumi](https://www.pulumi.com).

## Behavior

### check

Checks the version of the Pulumi stack.

#### parameters

- **stack_name**: Pulumi stack name
- **project_name**: Pulumi project name
- **source_dir**: optional source directory containing the target Pulumi files

### in

Writes a JSON-formatted file to the resource with the Pulumi stack outputs. This file is located at `<concourse working dir>/<pulumi source dir>/<pulumi stack name>_outputs.json`.

#### parameters

- **stack_name**: Pulumi stack name
- **project_name**: Pulumi project name
- **source_dir**: optional source directory containing the target Pulumi files

### out

Creates, updates, or destroys a Pulumi stack.

#### parameters

- **action**: Pulumi action; must be one of 'create', 'update', or 'destroy'
- **preview**: optional boolean to instead perform a dry-run update to a stack and return pending changes; only effective with 'create' or 'update' (default: false)
- **stack_name**: Pulumi stack name
- **project_name**: Pulumi project name
- **source_dir**: optional source directory containing the target Pulumi files
- **stack_config**: hash/dictionary that contains stack configuration key-value pairs
- **refresh_stack**: optional boolean to determine whether to refresh the Pulumi stack prior to action (default: `true`)
