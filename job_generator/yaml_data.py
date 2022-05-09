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

    def __init__(self, project_name: str, model_name: str, model_type: HydrologicalModelEnum):
        self.job_name = YamlData._create_job_name(model_name)
        self.namespace = str(model_type)
        self.container_image = YamlData._select_docker_image(model_type)
        self.container_name = YamlData._create_container_name(project_name, model_name)
        self.mount_path = YamlData._get_mount_path(model_type)
        self.args = YamlData._get_launch_args(model_type)
        self.sub_path = YamlData._get_mount_subpath(project_name, model_name, model_type)
        self.hydro_program = str(model_type)
        self.description = YamlData._create_sample_description()

    @staticmethod
    def _create_job_name(model_name: str) -> str:
        return f"{model_name}-{uuid.uuid4().hex[:YamlData.SHORTENED_UUID_LENGTH]}"

    @staticmethod
    def _create_container_name(project_name: str, model_name: str) -> str:
        return f"{project_name}-{model_name}"

    @staticmethod
    def _select_docker_image(model_type: HydrologicalModelEnum) -> str:
        if model_type is HydrologicalModelEnum.HYDRUS:
            return YamlData.HYDRUS_IMAGE
        elif model_type is HydrologicalModelEnum.MODFLOW:
            return YamlData.MODFLOW_IMAGE

    @staticmethod
    def _get_mount_path(model_type: HydrologicalModelEnum) -> str:
        if model_type is HydrologicalModelEnum.HYDRUS:
            return YamlData.HYDRUS_VOLUME_MOUNT
        elif model_type is HydrologicalModelEnum.MODFLOW:
            return YamlData.MODFLOW_VOLUME_MOUNT

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
