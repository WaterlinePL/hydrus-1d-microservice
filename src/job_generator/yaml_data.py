import uuid
from typing import List
from strenum import StrEnum

import job_manager


class HydrologicalModelEnum(StrEnum):
    MODFLOW = "modflow"
    HYDRUS = "hydrus"


class YamlData:
    SHORTENED_UUID_LENGTH = 21

    def __init__(self, job_prefix: str,
                 container_image: str,
                 container_name: str,
                 mount_path: str,
                 description: str):
        self.job_name = YamlData._create_job_name(job_prefix)
        self.container_image = container_image
        self.container_name = container_name
        self.mount_path = mount_path
        self.args = ["hflow-job-execute", f"wf:{self.job_name}", f"//{job_manager.REDIS_URL}"]
        self.extra_args = {}
        self.description = description

    def set_mount_sub_path(self, mount_sub_path: str):
        self.extra_args["sub_path"] = mount_sub_path

    def set_env(self, env):
        self.extra_args["env"] = env

    @staticmethod
    def _create_job_name(job_prefix: str) -> str:
        return f"{job_prefix}-{uuid.uuid4().hex[:YamlData.SHORTENED_UUID_LENGTH]}"
