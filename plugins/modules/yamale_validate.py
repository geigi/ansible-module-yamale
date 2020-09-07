#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 sipgate GmbH, <bearmetal@sipgate.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: yamale_validate
short_description: Validate YAML files against a schema definition
description:
  - validate YAML files against a schema definition using yamale
author: sipgate GmbH (bearmetal@sipgate.de)
requirements:
  - "python >= 3.6"
  - "yamale >= 3.0.4"
options:
    schema_path:
        description:
          - path to a YAML schema definition
        required: true
        type: str
    data_path:
        description:
          - path to the YAML file you want to validate
        required: true
        type: str
'''

EXAMPLES = r'''
---
- name: validate sample YAML file
  yamale_validate:
      schema_path: /path/to/schema.yaml
      data_path: /path/to/data.yaml
'''

RETURN = r'''
changed:
    description: Always false, this module does not carry out any changes.
    returned: always
    type: bool
msg:
    description: If the module fails, this will contain a short error description
    type: string
'''

from ansible.module_utils.basic import AnsibleModule

# TODO: fail if module not present
import yamale

def load_data(data_path):
    return yamale.make_data(data_path)
    

def load_schema(schema_path):
    return yamale.make_schema(schema_path)

def validate_yaml(data, schema):
    try:
        yamale.validate(schema, data)
        return True, ""
    except ValueError as e:
        return False, str(e)

def main():
    module_args = dict(
        data_path=dict(type='str', required=True),
        schema_path=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    data = load_data(module.params['data_path'])

    schema = load_schema(module.params['schema_path'])

    yamale_result, message = validate_yaml(data, schema)

    result = dict(
        changed=False,
        msg=message,
    )

    if yamale_result:
        module.exit_json(**result)
    else:
        module.fail_json(**result)


if __name__ == '__main__':
    main()
