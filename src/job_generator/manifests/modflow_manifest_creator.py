import json
from typing import Dict, Tuple

from job_generator.manifests.abstract_manifest_creator import AbstractManifestCreator, YamlManifest, JobName
from job_generator.yaml_data import YamlData, HydrologicalModelEnum
from job_generator.yaml_job_generator import YamlJobGenerator


class ModflowManifestCreator(AbstractManifestCreator):

    DOCKER_IMAGE = "watermodelling/modflow-job:latest"
    CONTAINER_NAME = "modflow"
    MOUNT_PATH = "/workspace"

    def __init__(self, project_name: str, modflow_model: str):
        super().__init__(project_name=project_name,
                         container_image=ModflowManifestCreator.DOCKER_IMAGE,
                         container_name=ModflowManifestCreator.CONTAINER_NAME,
                         mount_path=ModflowManifestCreator.MOUNT_PATH)
        self.modflow_model = modflow_model

    def _get_job_prefix(self) -> str:
        return self.modflow_model

    def create_manifest(self) -> Tuple[YamlManifest, JobName]:
        yaml_data = YamlData(job_prefix=self._get_job_prefix(),
                             container_image=self.container_image,
                             container_name=self.container_name,
                             mount_path=self.mount_path,
                             args=[],
                             description=f"Modflow simulation for {self.modflow_model}")
        return YamlJobGenerator.prepare_kubernetes_job(yaml_data), yaml_data.job_name

    def get_redis_command(self) -> str:
        cmd = {
            "executable": "bash",
            "args": [],     # TODO: get modflow ready
            "inputs": [],
            "outputs": []
        }
        return json.dumps(cmd)

