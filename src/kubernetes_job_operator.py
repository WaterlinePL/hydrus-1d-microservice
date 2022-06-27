from typing import List

import kubernetes.client
import logging

from job_generator import yaml_job_generator, job_spawner
from job_generator.yaml_data import YamlData, HydrologicalModelEnum

# config.load_incluster_config()
# config.load_config()


# CORE_API = client.CoreV1Api()
logging.basicConfig()

JOB_NAMESPACE = "simulation-jobs"  # TODO: Simulation namespace (ENV variable?)

JobName = str
ModelName = str


# TODO: Consider changing model to models (list)
def create_hydrus_job(project_name: str, hydrus_model: ModelName) -> JobName:
    with kubernetes.client.ApiClient() as api:
        batch_api = kubernetes.client.BatchV1Api(api)
        manifest = job_spawner.create_hydrus_job_manifest()
        # print(manifests)
        batch_api.create_namespaced_job(JOB_NAMESPACE, manifest)  # TODO: create this namespace
        return simulation_data.job_name


def create_modflow_job(project_name: str, modflow_model: str) -> JobName:
    with kubernetes.client.ApiClient() as api:
        batch_api = kubernetes.client.BatchV1Api(api)
        simulation_data = YamlData(project_name, modflow_model, HydrologicalModelEnum.MODFLOW)
        manifest = yaml_job_generator.YamlJobGenerator.prepare_kubernetes_job(simulation_data)
        # print(manifests)
        batch_api.create_namespaced_job(JOB_NAMESPACE, manifest)  # TODO: create this namespace
        return simulation_data.job_name


# FIXME: placeholder
def create_file_download_job(project_name: str) -> JobName:
    with kubernetes.client.ApiClient() as api:
        batch_api = kubernetes.client.BatchV1Api(api)
        body = {"TODO": "todo"}  # TODO: create job manifests for file download job
        batch_api.create_namespaced_job(JOB_NAMESPACE, body)  # TODO: create this namespace
        return body["name"]  # TODO: maybe a class


# FIXME: placeholder
def create_file_removal_job(project_name: str) -> JobName:
    with kubernetes.client.ApiClient() as api:
        batch_api = kubernetes.client.BatchV1Api(api)
        body = {"TODO": "todo"}  # TODO: create job manifests for file download job
        batch_api.create_namespaced_job(JOB_NAMESPACE, body)  # TODO: create this namespace
        return body["name"]  # TODO: maybe a class
