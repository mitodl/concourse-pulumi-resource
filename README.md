# Concourse Pulumi Resource

A [concourse-ci](https://concourse-ci.org) resource for provisioning infrastructure via [Pulumi](https://www.pulumi.com).

## Behavior

### check

Checks the version of the Pulumi stack.

#### parameters

- **stack_name**: Pulumi stack name
- **project_name**: Pulumi project name
- **source_dir**: optional source directory containing the target Pulumi files
- **env_os**: optional hash/dictionary containing os in-process environment variable key-value pairs

### in

Writes a JSON-formatted file to the resource with the Pulumi stack outputs. This file is located at `<concourse working dir>/<pulumi source dir>/<pulumi stack name>_outputs.json`.

#### parameters

- **stack_name**: Pulumi stack name
- **project_name**: Pulumi project name
- **source_dir**: optional source directory containing the target Pulumi files
- **env_pulumi**: optional hash/dictionary containing Pulumi environment variable key-value pairs
- **env_os**: optional hash/dictionary containing os in-process environment variable key-value pairs

### out

Creates, updates, or destroys a Pulumi stack.

#### parameters

- **action**: Pulumi action; must be one of 'create', 'update', or 'destroy'
- **preview**: optional boolean to instead perform a dry-run update to a stack and return pending changes; only effective with 'create' or 'update' (default: false)
- **stack_name**: Pulumi stack name
- **project_name**: Pulumi project name
- **source_dir**: optional source directory containing the target Pulumi files
- **stack_config**: optional hash/dictionary that contains stack configuration key-value pairs
- **env_pulumi**: optional hash/dictionary containing Pulumi environment variable key-value pairs
- **env_os**: optional hash/dictionary containing os in-process environment variable key-value pairs
- **refresh_stack**: optional boolean to determine whether to refresh the Pulumi stack prior to action (default: `true`)

## Example

```yaml
---
resource_types:
- name: pulumi
  type: docker-image
  source:
    repository: mitodl/concourse-pulumi-resource
    tag: latest

resources:
- name: pulumi-thing-doer
  type: pulumi

jobs:
- name: pulumi-stuff-and-things
  plan:
  - get: pulumi_files
  - put: pulumi-thing-doer
    params:
      action: update
      stack_name: applications.sign_and_verify.QA
      project_name: ol-infrastructure-sign-and-verify-application
      source_dir: pulumi_files/src/ol_infrastructure/applications/sign_and_verify
      env_pulumi:
        AWS_REGION: us-east-1
      env_os:
        PATH: "${PATH}:/usr/local/bin"
```
