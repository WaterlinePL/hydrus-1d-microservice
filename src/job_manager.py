import os
from typing import List

import kubernetes as kubernetes
from werkzeug.exceptions import abort

import config
from job_generator.manifests.abstract_manifest_creator import AbstractManifestCreator
from job_generator.manifests.cleanup_manifest_creator import ProjectCleanupManifestCreator
from job_generator.manifests.download_manifest_creator import ProjectDownloadManifestCreator
from job_generator.manifests.hydrus_manifest_creator import HydrusManifestCreator
from job_generator.manifests.modflow_manifest_creator import ModflowManifestCreator
from job_generator.yaml_job_generator import JobManifestGenerator
from redis_operator import RedisOperator, JobStatus

ModelName = str
JobId = str


class JobManager:
    def __init__(self, redis_url: str):
        self.redis_operator = RedisOperator(redis_url)

    def create_download_job(self, project_name: str, hydrus_models: List[ModelName], modflow_model: ModelName) -> JobId:
        manifest_creator = ProjectDownloadManifestCreator(project_name, hydrus_models, modflow_model)
        return self._deploy_job(manifest_creator)

    def create_hydrus_job(self, project_name: str, hydrus_model: ModelName) -> JobId:
        manifest_creator = HydrusManifestCreator(project_name, hydrus_model)
        return self._deploy_job(manifest_creator)

    def create_modflow_job(self, project_name: str, modflow_model: ModelName, spin_up: int) -> JobId:
        manifest_creator = ModflowManifestCreator(project_name, modflow_model, spin_up)
        return self._deploy_job(manifest_creator)

    def create_cleanup_job(self, project_name: str) -> JobId:
        manifest_creator = ProjectCleanupManifestCreator(project_name)
        return self._deploy_job(manifest_creator)

    def check_job(self, job_id: str):
        status = self.redis_operator.get_job_status(job_id)
        if status == JobStatus.NOT_FOUND:
            abort(404)
        return status

    def _deploy_job(self, manifest_creator: AbstractManifestCreator):
        manifest, job_name = manifest_creator.create_manifest()
        self.redis_operator.put_job_command(f"wf:{job_name}_msg", manifest_creator.get_redis_command())
        with kubernetes.client.ApiClient() as api:
            batch_api = kubernetes.client.BatchV1Api(api)
            batch_api.create_namespaced_job(config.SIMULATION_NAMESPACE, manifest)
            return job_name


job_manager = JobManager(config.REDIS_URL)
