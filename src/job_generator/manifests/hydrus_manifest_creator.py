import json
from typing import Dict, Tuple

from job_generator.manifests.abstract_manifest_creator import AbstractManifestCreator, YamlManifest, JobName
from job_generator.yaml_data import YamlData, HydrologicalModelEnum
from job_generator.yaml_job_generator import JobManifestGenerator


class HydrusManifestCreator(AbstractManifestCreator):

    DOCKER_IMAGE = "watermodelling/hydrus-job:latest"
    CONTAINER_NAME = "hydrus"
    MOUNT_PATH = "/workspace"

    def __init__(self, project_name: str, hydrus_model: str):
        super().__init__(project_name=project_name,
                         container_image=HydrusManifestCreator.DOCKER_IMAGE,
                         container_name=HydrusManifestCreator.CONTAINER_NAME,
                         mount_path=HydrusManifestCreator.MOUNT_PATH)
        self.hydrus_model = hydrus_model

    def _get_job_prefix(self) -> str:
        return self.hydrus_model

    def create_manifest(self) -> Tuple[YamlManifest, JobName]:
        yaml_data = YamlData(job_prefix=self._get_job_prefix(),
                             container_image=self.container_image,
                             container_name=self.container_name,
                             mount_path=self.mount_path,
                             description=f"Hydrus simulation for {self.hydrus_model}")
        yaml_data.set_mount_sub_path(f"{self.project_name}/{HydrologicalModelEnum.HYDRUS}/{self.hydrus_model}")
        return JobManifestGenerator.prepare_kubernetes_job(yaml_data), yaml_data.job_name

    def get_redis_command(self) -> str:
        cmd = {
            "executable": "./hydrus",
            "args": [],
            "inputs": [],
            "outputs": []
        }
        return json.dumps(cmd)
