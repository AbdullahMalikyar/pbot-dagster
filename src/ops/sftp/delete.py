from datetime import datetime

from dagster import In, List, Nothing, OpExecutionContext, op, String

from resources.ssh import SSHClientResource

COMMON_CONFIG = dict(required_resource_keys=["sftp"])


@op(**COMMON_CONFIG, ins={"file": In(String), "nonce": In(Nothing)})
def delete(context: OpExecutionContext, file: str) -> str:
    trace = datetime.now()

    sftp: SSHClientResource = context.resources.sftp

    context.log.info(f"Will remove {file}...")

    sftp.remove(file)

    context.log.info(f" 🚗 Deleted file in {datetime.now() - trace}.")

    return file


@op(**COMMON_CONFIG, ins={"files": In(List), "nonce": In(Nothing)})
def delete_list(context: OpExecutionContext, files: list[str]) -> list[str]:
    trace = datetime.now()

    sftp: SSHClientResource = context.resources.sftp

    context.log.info(f"Will remove {len(files)} files...")

    for file in files:
        sftp.remove(file)

    context.log.info(f" 🚗 Deleted {len(files)} files in {datetime.now() - trace}.")

    return files
