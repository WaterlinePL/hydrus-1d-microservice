import json
import os
import unittest
from typing import Dict, Any, Tuple

import config
from job_generator.manifests import minio_secret_ref
from job_generator.yaml_data import YamlData
from job_generator.yaml_job_generator import JobManifestGenerator


class TestJobGenerator(unittest.TestCase):

    def test_base_manifest(self):
        yaml_data = TestJobGenerator._create_sample_base_yaml_data()
        self.assertEqual(*TestJobGenerator._create_expected_and_actual_manifest(yaml_data))

    def test_with_env(self):
        yaml_data = TestJobGenerator._create_sample_base_yaml_data()
        yaml_data.set_env([minio_secret_ref.endpoint, minio_secret_ref.access_key, minio_secret_ref.secret_key])
        self.assertEqual(*TestJobGenerator._create_expected_and_actual_manifest(yaml_data))

    def test_with_sub_path(self):
        yaml_data = TestJobGenerator._create_sample_base_yaml_data()
        yaml_data.set_mount_sub_path("mount/sub/path")
        self.assertEqual(*TestJobGenerator._create_expected_and_actual_manifest(yaml_data))

    def test_with_sub_path_and_env(self):
        yaml_data = TestJobGenerator._create_sample_base_yaml_data()
        yaml_data.set_env([minio_secret_ref.endpoint, minio_secret_ref.access_key, minio_secret_ref.secret_key])
        yaml_data.set_mount_sub_path("mount/sub/path")
        self.assertEqual(*TestJobGenerator._create_expected_and_actual_manifest(yaml_data))

    @staticmethod
    def _create_expected_and_actual_manifest(yaml_data: YamlData) -> Tuple[Dict, Dict]:
        expected = TestJobGenerator._generate_expected_manifest(yaml_data=yaml_data,
                                                                namespace=config.SIMULATION_NAMESPACE,
                                                                pvc_name=config.PVC_NAME,
                                                                redis_url=config.REDIS_URL)
        actual = JobManifestGenerator.prepare_kubernetes_job(yaml_data)
        return expected, actual

    @staticmethod
    def _create_sample_base_yaml_data() -> YamlData:
        return YamlData(job_prefix="sample-job",
                        docker_image="sample-image",
                        container_name="sample-container-name",
                        description="Sample description of the job")

    @staticmethod
    def _generate_expected_manifest(yaml_data: YamlData,
                                    namespace: str,
                                    pvc_name: str,
                                    redis_url: str) -> Dict[str, Any]:
        containers = [{
            'name': yaml_data.container_name,
            'image': yaml_data.docker_image,
            'imagePullPolicy': "Always",
            'args': ["hflow-job-execute", yaml_data.task_id, f"//{redis_url}"],
            'volumeMounts': [{
                'mountPath': "/workspace",
                'name': "simulation-volume"
                # 'subPath': data.extra_args['sub_path']    # only if specified
            }],
        }]

        if "sub_path" in yaml_data.extra_args:
            # Somehow hacky
            containers[0]['volumeMounts'][0]['subPath'] = yaml_data.extra_args["sub_path"].split('subPath:')[1].lstrip()
        if "env" in yaml_data.extra_args:
            # Significantly hacky :(
            containers[0]["env"] = json.loads(yaml_data.extra_args["env"]
                                              .split('env:')[1].lstrip()
                                              .replace("'", '"')
                                              .replace("False", "false"))

        volumes = [{
            'name': "simulation-volume",
            'persistentVolumeClaim': {
                'claimName': pvc_name
            }
        }]

        spec = {
            'volumes': volumes,
            'containers': containers,
            'restartPolicy': 'Never'
        }

        return {
            'apiVersion': 'batch/v1',
            'kind': 'Job',
            'metadata': {
                'name': yaml_data.job_name,
                'namespace': namespace,
                'annotations': {
                    'description': yaml_data.description
                }
            },
            'spec': {
                'backoffLimit': config.BACKOFF_LIMIT,
                'template': {
                    'ttlSecondsAfterFinished': config.JOB_TTL_IN_SEC,
                    'spec': spec
                }
            }
        }
