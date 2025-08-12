from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from typing import Optional
import boto3
import botocore

MAX_DELETE = 1000

DOCUMENTATION = """
    module: status
    short_description: Custom plugin to delete Cloudflare R2 objects
    description: Custom plugin to get volume status
    options:
        bucket_name:
            description: Bucket name
            required: true
            type: str
        access_key:
            description: AWS Access key ID
            required: true
            type: str
        secret_key:
            description: AWS Secret Access key
            required: true
            type: str
        endpoint_url:
            description: Cloudflare R2 endpoint URL
            required: true
            type: str
        region:
            description: Cloudflare R2 region
            required: false
            type: str
"""

def delete_objects(access_key: str, endpoint_url: str, secret_key: str, bucket_name: str, 
                   region: str = "auto"):

    session_args = dict(
        service_name = "s3",
        region_name = region,
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        endpoint_url = endpoint_url
    )

    s3 = boto3.client(**session_args)

    s3_buckets_response = s3.list_buckets()

    s3_buckets = [bucket["Name"] for bucket in s3_buckets_response["Buckets"]]

    changed = False
    deleted_objects = []

    if bucket_name in s3_buckets:
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket_name)
        objects = []

        for page in pages:
            if "Contents" in page:
                objects = [{"Key": obj["Key"]} for obj in page["Contents"]]

                for i in range(0, len(objects), MAX_DELETE):
                    chunk = objects[i:i+MAX_DELETE]
                    if not chunk:
                        continue
                    resp = s3.delete_objects(Bucket=bucket_name, Delete={"Objects": chunk, "Quiet": True})
                    deleted_objects += [d.get("Key") for d in resp.get("Deleted", [])]
                changed = True

        msg = "Objects were deleted" if changed else "There are no objects to delete"

    else:
        msg = "Bucket does not exist"

    return changed, msg, deleted_objects

def run_module():

    module_args = {
        "region": {"default": "auto", "type": "str"},
        "access_key": {"required": True, "type": "str", "no_log": True},
        "secret_key": {"required": True, "type": "str", "no_log": True},
        "bucket_name": {"required": True, "type": "str"},
        "endpoint_url": {"required": True, "type": "str"}
    }

    params = {}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    for key, value in module_args.items():
        params[key] = module.params[key]

    try:
        changed, msg, delete_output = delete_objects(**params)
        result = dict(
            changed=changed,
            msg=msg,
            ansible_module_results=delete_output
        )
        module.exit_json(**result)

    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=f"S3 error: {str(e)}", changed=False)
    
    except Exception as e:
        module.fail_json(msg=f"Unexpected error: {str(e)}", changed=False)

def main():
    run_module()

if __name__ == '__main__':
    main()
