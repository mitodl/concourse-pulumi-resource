"""the concourse functions and methods for the three primary commands, and their interfacing with the pulumi automation api bindings interface"""
import sys
import os
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
    # TODO: it looks like this should be a dummy, but should it really?
    payload = {
        'version': 'placeholder',
        'metadata': '',
    }
    json.dump(payload, sys.stdout)


def out_cmd():
    """concourse out command"""
    # assign input parameters
    params = __read_params()
    # determine current working dir
    working_dir = sys.argv[1]
    # create or update pulumi stack
    lib.pulumi.create_update_stack(
        stack_name=params['stack_name'],
        project_name=params['project_name'],
        # TODO: use new path lib thing for python
        source_dir=os.path.join(working_dir, params['source_dir']),
        cloud_config=params['cloud_config']
    )
    # dump out json payload
    # TODO: use pulumi outputs for this
    payload = {
        'version': 'placeholder',
        'metadata': '',
    }
    json.dump(payload, sys.stdout)


def __read_params(stream=sys.stdin):
    inputs = json.load(stream)
    return inputs['params']
