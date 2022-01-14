# Concourse Pulumi Resource

A [concourse-ci](https://concourse-ci.org) resource for provisioning infrastructure via [Pulumi](https://www.pulumi.com).

## Behavior

### check

Checks the version of the Pulumi stack.

#### parameters

- **stack_name**: Pulumi stack name
- **project_name**: Pulumi project name

### in

Writes a JSON-formatted file to the resource with the Pulumi stack outputs.

#### parameters

- **stack_name**: Pulumi stack name
- **project_name**: Pulumi project name

### out

Creates, updates, or destroys a Pulumi stack.

#### parameters

- **action**: Pulumi action; must be one of 'create', 'update', or 'destroy'
- **stack_name**: Pulumi stack name
- **project_name**: Pulumi project name
- **source_dir**: source directory containing the target Pulumi files
- **cloud_config**: contains cloud configuration information
  - **aws_region**: AWS region in which to create or update the Pulumi stack
- **refresh_stack**: boolean to determine whether to refresh the Pulumi stack prior to action
