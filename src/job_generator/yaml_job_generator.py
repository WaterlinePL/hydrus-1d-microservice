import os
from typing import Dict

import yaml
from jinja2 import Environment, FileSystemLoader

import config
from job_generator.yaml_data import YamlData

YamlManifest = Dict[str, str]


class JobManifestGenerator:

    @staticmethod
    def prepare_kubernetes_job(data: YamlData) -> YamlManifest:
        templating_env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True)
        template = templating_env.get_template("job_template.yaml")
        return yaml.safe_load(template.render(job_name=data.job_name,
                                              job_namespace=config.SIMULATION_NAMESPACE,
                                              job_description=data.description,
                                              pvc_name=config.PVC_NAME,
                                              container_name=data.container_name,
                                              docker_image=data.docker_image,
                                              task_id=data.task_id,
                                              redis_url=f"//{config.REDIS_URL}",
                                              backoff_limit=config.BACKOFF_LIMIT,
                                              job_ttl_in_sec=config.JOB_TTL_IN_SEC,
                                              **data.extra_args))
