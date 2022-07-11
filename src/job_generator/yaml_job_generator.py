import os
from typing import Dict

from job_generator.yaml_data import YamlData

YamlManifest = Dict[str, str]


class YamlJobGenerator:
    # IMPORTANT: create env variable 'NFS_PVC' with name of PVC
    PVC_NAME = os.environ['NFS_PVC']
    VOLUME_NAME = "simulation-volume"
    BACKOFF_LIMIT = 2

    @staticmethod
    def prepare_kubernetes_job(data: YamlData) -> YamlManifest:
        containers = [{
            'image': data.container_image,
            'name': data.container_name,
            'imagePullPolicy': "Always",
            'volumeMounts': [{
                'mountPath': data.mount_path,
                'name': YamlJobGenerator.VOLUME_NAME
                # 'subPath': data.extra_args['sub_path']    # only if specified
            }],
            'args': data.args
        }]

        if "sub_path" in data.extra_args:
            containers[0]['volumeMounts'][0]['subPath'] = data.extra_args['sub_path']
        if "env" in data.extra_args:
            containers[0]["env"] = data.extra_args["env"]

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
