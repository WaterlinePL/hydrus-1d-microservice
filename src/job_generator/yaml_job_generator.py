import os
from typing import Dict

from src.job_generator.yaml_data import YamlData

YamlManifest = Dict[str, str]


class YamlJobGenerator:
    # IMPORTANT: create env variable 'PVC' with name of PVC
    # (default from .yaml: 'nfs-pvc')
    PVC_NAME = os.environ['PVC']
    VOLUME_NAME = "project-volume"
    BACKOFF_LIMIT = 2

    @staticmethod
    def prepare_kubernetes_job(data: YamlData) -> YamlManifest:
        containers = [{
            'image': data.container_image,
            'name': data.container_name,
            'volumeMounts': [{
                'mountPath': data.mount_path,
                'name': YamlJobGenerator.VOLUME_NAME,
                'subPath': data.sub_path
            }],
            'args': data.args
        }]

        volumes = [{
            'name': YamlJobGenerator.VOLUME_NAME,
            'persistentVolumeClaim': {
                'claimName': YamlJobGenerator.PVC_NAME
            }
        }]

        spec = {
            'containers': containers,
            'volumes': volumes,
            'restartPolicy': 'Never'
        }

        config = {
            'apiVersion': 'batch/v1',
            'kind': 'Job',
            'metadata': {
                'name': data.job_name,
                'annotations': {
                    'program': data.hydro_program,
                    'description': data.description
                }
            },
            'spec': {
                'template': {
                    'spec': spec
                },
                'backoffLimit': YamlJobGenerator.BACKOFF_LIMIT
            }
        }

        return config
