import json
from typing import Dict, Tuple

from job_generator.manifests.abstract_manifest_creator import AbstractManifestCreator, YamlManifest, JobName
from job_generator.yaml_data import YamlData, HydrologicalModelEnum
from job_generator.yaml_job_generator import JobManifestGenerator


class ModflowManifestCreator(AbstractManifestCreator):

    DOCKER_IMAGE = "watermodelling/modflow-job:latest"
    CONTAINER_NAME = "modflow"

    def __init__(self, project_name: str, modflow_model: str, spin_up: int):
        super().__init__(project_name=project_name,
                         container_image=ModflowManifestCreator.DOCKER_IMAGE,
                         container_name=ModflowManifestCreator.CONTAINER_NAME)
        self.modflow_model = modflow_model
        self.spin_up = spin_up

    def _get_job_prefix(self) -> str:
        return self.modflow_model

    def create_manifest(self) -> Tuple[YamlManifest, JobName]:
        yaml_data = YamlData(job_prefix=self._get_job_prefix(),
                             docker_image=self.docker_image,
                             container_name=self.container_name,
                             description=f"Modflow simulation for {self.modflow_model}")
        return JobManifestGenerator.prepare_kubernetes_job(yaml_data), yaml_data.job_name

    def get_redis_command(self) -> str:
        cmd = {
            "executable": "bash",
            "args": ["launch_modflow.sh", self.project_name, self.modflow_model, self.spin_up],
            "inputs": [],
            "outputs": []
        }
        return json.dumps(cmd)
