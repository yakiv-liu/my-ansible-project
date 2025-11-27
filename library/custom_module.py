#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            message=dict(type='str', required=True),
            repeat=dict(type='int', default=1)
        )
    )
    
    message = module.params['message']
    repeat = module.params['repeat']
    
    result = dict(
        changed=False,
        original_message=message,
        repeated_message=message * repeat,
        message="Task completed successfully"
    )
    
    module.exit_json(**result)

if __name__ == '__main__':
    main()
