"""the concourse functions and methods for the three primary commands, and their interfacing with the pulumi automation api bindings interface"""
import sys
import pathlib
import json

import lib.pulumi


def check_cmd():
    """concourse check command"""
    # assign input parameters
    params = __read_params()

    # read version value from stack
    version = lib.pulumi.read_stack(
        stack_name=params['stack_name'],
        project_name=params['project_name'],
        output_key='version'
    )

    # dump out json payload
    json.dump({'version': version}, sys.stdout)


def in_cmd():
    """concourse in command"""
    # assign input parameters
    params = __read_params()
    # read all outputs from stack
    outputs = lib.pulumi.read_stack(
        stack_name=params['stack_name'],
        project_name=params['project_name']
    )

    # create payload with stack version and stack outputs metadata
    payload = {
        'version': outputs['version'].value,
        'metadata': {
            params['stack_name']: outputs
        },
    }
    # TODO: dump to resource file
    json.dump(payload, sys.stdout)


def out_cmd():
    """concourse out command"""
    # assign input parameters
    params = __read_params()
    # determine current working dir
    working_dir = sys.argv[1]
    # create or update pulumi stack
    if params['action'] == 'create' or params['action'] == 'update':
        lib.pulumi.create_update_stack(
            stack_name=params['stack_name'],
            project_name=params['project_name'],
            source_dir=pathlib.Path(working_dir).joinpath(params['source_dir']),
            cloud_config=params['cloud_config'],
            refresh_stack=params['refresh_stack']
        )
    elif params['action'] == 'destroy':
        lib.pulumi.destroy_stack(
            stack_name=params['stack_name'],
            project_name=params['project_name'],
            refresh_stack=params['refresh_stack']
        )
    else:
        raise RuntimeError('Invalid value for "action" parameter')
    # dump out json payload
    # TODO: determine what this should be
    payload = {
        'version': 'placeholder',
        'metadata': '',
    }
    json.dump(payload, sys.stdout)


def __read_params(stream=sys.stdin):
    inputs = json.load(stream)
    return inputs['params']
