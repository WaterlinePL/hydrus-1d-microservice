import json
from typing import Dict, Tuple, List

from job_generator.manifests import minio_secret_ref
from job_generator.manifests.abstract_manifest_creator import AbstractManifestCreator, YamlManifest, JobName
from job_generator.yaml_data import YamlData
from job_generator.yaml_job_generator import YamlJobGenerator


class ProjectDownloadManifestCreator(AbstractManifestCreator):

    DOCKER_IMAGE = "watermodelling/project-download-job:latest"
    CONTAINER_NAME = "project-download"
    MOUNT_PATH = "/workspace"

    ENV = [
        minio_secret_ref.endpoint,
        minio_secret_ref.access_key,
        minio_secret_ref.secret_key
    ]

    def __init__(self, project_name: str, hydrus_models: List[str], modflow_model: str):
        super().__init__(project_name=project_name,
                         container_image=ProjectDownloadManifestCreator.DOCKER_IMAGE,
                         container_name=ProjectDownloadManifestCreator.CONTAINER_NAME,
                         mount_path=ProjectDownloadManifestCreator.MOUNT_PATH)
        self.hydrus_models = hydrus_models
        self.modflow_model = modflow_model

    def _get_job_prefix(self) -> str:
        return f"download-{self.project_name}"

    def create_manifest(self) -> Tuple[YamlManifest, JobName]:
        yaml_data = YamlData(job_prefix=self._get_job_prefix(),
                             container_image=self.container_image,
                             container_name=self.container_name,
                             mount_path=self.mount_path,
                             description=f"Download job for project: {self.project_name}")
        yaml_data.extra_args["env"] = ProjectDownloadManifestCreator.ENV
        return YamlJobGenerator.prepare_kubernetes_job(yaml_data), yaml_data.job_name

    def get_redis_command(self) -> str:
        args = ["download_project.sh", self.project_name, f"modflow:{self.modflow_model}"]

        for model in self.hydrus_models:
            args.append(f"hydrus:{model}")

        cmd = {
            "executable": "bash",
            "args": args,
            "inputs": [],
            "outputs": []
        }
        return json.dumps(cmd)
