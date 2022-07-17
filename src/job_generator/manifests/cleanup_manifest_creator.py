import json
from typing import Dict, Tuple, List

from job_generator.manifests import minio_secret_ref
from job_generator.manifests.abstract_manifest_creator import AbstractManifestCreator, YamlManifest, JobName
from job_generator.yaml_data import YamlData, HydrologicalModelEnum
from job_generator.yaml_job_generator import JobManifestGenerator


class ProjectCleanupManifestCreator(AbstractManifestCreator):

    DOCKER_IMAGE = "watermodelling/project-cleanup-job:latest"
    CONTAINER_NAME = "project-cleanup"

    ENV = [
        minio_secret_ref.endpoint,
        minio_secret_ref.access_key,
        minio_secret_ref.secret_key
    ]

    def __init__(self, project_name: str):
        super().__init__(project_name=project_name,
                         docker_image=ProjectCleanupManifestCreator.DOCKER_IMAGE,
                         container_name=ProjectCleanupManifestCreator.CONTAINER_NAME)

    def _get_job_prefix(self) -> str:
        return f"cleanup-{self.project_name}"

    def create_manifest(self) -> Tuple[YamlManifest, JobName]:
        yaml_data = YamlData(job_prefix=self._get_job_prefix(),
                             docker_image=self.docker_image,
                             container_name=self.container_name,
                             description=f"Cleanup job for project {self.project_name}")
        yaml_data.set_env(ProjectCleanupManifestCreator.ENV)
        return JobManifestGenerator.prepare_kubernetes_job(yaml_data), yaml_data.job_name

    def get_redis_command(self) -> str:
        cmd = {
            "executable": "bash",
            "args": ["project_cleanup.sh", self.project_name],
            "inputs": [],
            "outputs": []
        }
        return json.dumps(cmd)

