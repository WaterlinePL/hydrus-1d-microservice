import logging

from kubernetes.client import ApiException
from strenum import StrEnum

from job_generator import yaml_job_generator
from job_generator.yaml_data import YamlData, HydrologicalModelEnum
from kubernetes import config, client

# config.load_incluster_config()

# CORE_API = client.CoreV1Api()
BATCH_API = client.BatchV1Api()


class JobStatus(StrEnum):
    FAILED = "failed"
    SUCCESS = "success"
    NOT_FOUND = "not found"
    IN_PROGRESS = "in progress"


def create_job(project_name: str, model_name: str, model_type: HydrologicalModelEnum) -> str:
    simulation_data = YamlData(project_name, model_name, model_type)
    manifest = yaml_job_generator.YamlJobGenerator.prepare_kubernetes_job(simulation_data)
    BATCH_API.create_namespaced_job(simulation_data.namespace, manifest)
    return simulation_data.job_name


def get_job_status(job_name: str, namespace: str) -> JobStatus:
    try:
        job = BATCH_API.read_namespaced_job_status(job_name, namespace)
        completed = bool(job.status.succeeded)
        failed = bool(job.status.failed)

        if completed:
            return JobStatus.SUCCESS
        if failed:
            return JobStatus.FAILED

        return JobStatus.IN_PROGRESS

    except ApiException as error:
        if error.status == 404:
            # does not exist yet
            return JobStatus.NOT_FOUND
        else:
            logging.error(error.body)
            raise
