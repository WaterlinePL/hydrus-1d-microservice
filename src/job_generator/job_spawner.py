from job_generator.yaml_data import HydrologicalModelEnum, YamlData

ModelName = str


def create_download_job_manifest():
    pass


def create_hydrus_job_manifest(project_name: str, hydrus_model: ModelName):
    simulation_data = YamlData(project_name, hydrus_model, HydrologicalModelEnum.HYDRUS)
    manifest = yaml_job_generator.YamlJobGenerator.prepare_kubernetes_job(simulation_data)


def create_modflow_job_manifest():
    pass


def create_cleanup_job_manifest():
    pass
