import json
from typing import Dict, Tuple, List

from job_generator.manifests.abstract_manifest_creator import AbstractManifestCreator, YamlManifest, JobName
from job_generator.yaml_data import YamlData, HydrologicalModelEnum
from job_generator.yaml_job_generator import YamlJobGenerator


class ProjectCleanupManifestCreator(AbstractManifestCreator):

    DOCKER_IMAGE = "watermodelling/project-cleanup-job:latest"
    CONTAINER_NAME = "project-cleanup"
    MOUNT_PATH = "/workspace"

    def __init__(self, project_name: str):
        super().__init__(project_name=project_name,
                         container_image=ProjectCleanupManifestCreator.DOCKER_IMAGE,
                         container_name=ProjectCleanupManifestCreator.CONTAINER_NAME,
                         mount_path=ProjectCleanupManifestCreator.MOUNT_PATH)

    def _get_job_prefix(self) -> str:
        return f"cleanup-{self.project_name}"

    def create_manifest(self) -> Tuple[YamlManifest, JobName]:
        yaml_data = YamlData(job_prefix=self._get_job_prefix(),
                             container_image=self.container_image,
                             container_name=self.container_name,
                             mount_path=self.mount_path,
                             args=[],
                             description=f"Cleanup job for project: {self.project_name}")
        return YamlJobGenerator.prepare_kubernetes_job(yaml_data), yaml_data.job_name

    def get_redis_command(self) -> str:
        cmd = {
            "executable": "bash",
            "args": ["project_cleanup.sh", self.project_name],
            "inputs": [],
            "outputs": []
        }
        return json.dumps(cmd)

