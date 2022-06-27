import uuid
from typing import List
from strenum import StrEnum


class HydrologicalModelEnum(StrEnum):
    MODFLOW = "modflow"
    HYDRUS = "hydrus"


class YamlData:
    SHORTENED_UUID_LENGTH = 21

    HYDRUS_IMAGE = "watermodelling/hydrus-modflow-synergy-engine:hydrus1d_linux"
    HYDRUS_VOLUME_MOUNT = "/workspace/hydrus"

    MODFLOW_IMAGE = "mjstealey/docker-modflow"
    MODFLOW_VERSION = "mf2005"
    MODFLOW_VOLUME_MOUNT = "/workspace"

    def __init__(self, job_prefix: str,
                 container_image: str,
                 container_name: str,
                 mount_path: str,
                 args: List[str],
                 description: str):
        self.job_name = YamlData._create_job_name(job_prefix)
        self.container_image = container_image
        self.container_name = container_name
        self.mount_path = mount_path
        self.args = args
        self.extra_args = {}
        self.description = description

    def set_mount_sub_path(self, mount_sub_path: str):
        self.extra_args["sub_path"] = mount_sub_path

    @staticmethod
    def _create_job_name(job_prefix: str) -> str:
        return f"{job_prefix}-{uuid.uuid4().hex[:YamlData.SHORTENED_UUID_LENGTH]}"

    @staticmethod
    def _get_mount_subpath(project_name: str, model_name: str, model_type: HydrologicalModelEnum) -> str:
        return f"{project_name}/{model_type}/{model_name}"

    @staticmethod
    def _create_sample_description() -> str:
        return "sample description"

    @staticmethod
    def _get_launch_args(model_type: HydrologicalModelEnum) -> List[str]:
        if model_type is HydrologicalModelEnum.HYDRUS:
            return []
        elif model_type is HydrologicalModelEnum.MODFLOW:
            return [YamlData.MODFLOW_VERSION, None]  # TODO: .nam file instead of None
