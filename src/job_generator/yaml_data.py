import uuid
from typing import List, Dict, Any
from strenum import StrEnum

# Formatted as in .yaml
YamlEnvVariable = Dict[str, Any]


class HydrologicalModelEnum(StrEnum):
    MODFLOW = "modflow"
    HYDRUS = "hydrus"


class YamlData:
    SHORTENED_UUID_LENGTH = 21

    def __init__(self, job_prefix: str,
                 docker_image: str,
                 container_name: str,
                 description: str):
        self.job_name = YamlData._create_job_name(job_prefix)
        self.docker_image = docker_image
        self.container_name = container_name
        self.task_id = f"wf:{self.job_name}"
        self.extra_args = {}
        self.description = description

    def set_mount_sub_path(self, mount_sub_path: str):
        self.extra_args["sub_path"] = f"subPath: {mount_sub_path}"

    def set_env(self, env_variable_list: List[YamlEnvVariable]):
        self.extra_args["env"] = f"env: {env_variable_list}"

    @staticmethod
    def _create_job_name(job_prefix: str) -> str:
        return f"{job_prefix}-{uuid.uuid4().hex[:YamlData.SHORTENED_UUID_LENGTH]}"
