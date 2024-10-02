import os

from datetime import datetime

from dagster import Field, OpExecutionContext, op, String

from resources.ssh import SSHClientResource

COMMON_CONFIG = dict(
    config_schema={
        "path": Field(String, description="path on the SFTP site to place this file")
    },
    required_resource_keys=["sftp"],
)


@op(**COMMON_CONFIG)
def put(context: OpExecutionContext, file: str) -> str:
    trace = datetime.now()

    sftp: SSHClientResource = context.resources.sftp

    context.log.info(f"Will upload {file}...")

    sftp.put(file, os.path.join(context.op_config["path"], os.path.basename(file)))

    context.log.info(f"Uploaded file in {datetime.now() - trace}.")

    return file
