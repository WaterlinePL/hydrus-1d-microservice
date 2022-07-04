from flask import Flask, request
from strenum import StrEnum
from kubernetes import config
from job_manager import job_manager

app = Flask(__name__)


class RestMethod(StrEnum):
    GET = 'GET'
    DELETE = 'DELETE'
    PUT = 'PUT'
    POST = 'POST'


@app.route("/project-files", methods=[RestMethod.POST, RestMethod.DELETE])
def manage_project_files():
    project_name = request.json["projectId"]
    if request.method == RestMethod.POST:
        hydrus_models = request.json["hydrusModels"]
        modflow_model = request.json["modflowModel"]
        return job_manager.create_download_job(project_name, hydrus_models, modflow_model)
    elif request.method == RestMethod.DELETE:
        return job_manager.create_cleanup_job(project_name)


@app.route("/simulation/hydrus", methods=[RestMethod.POST])
def launch_hydrus():
    project_name = request.json["projectId"]
    model = request.json["modelName"]
    return job_manager.create_hydrus_job(project_name, model)


@app.route("/simulation/modflow", methods=[RestMethod.POST])
def launch_modflow():
    project_name = request.json["modelDetails"]["projectId"]
    model = request.json["modelDetails"]["modelName"]
    spin_up = request.json["spinUp"]
    return job_manager.create_modflow_job(project_name, model, spin_up)


@app.route("/status/<job_id>", methods=[RestMethod.GET])
def get_simulation_job_status(job_id: str):
    return job_manager.check_job(job_id)


if __name__ == '__main__':
    # run flask app
    # config.load_kube_config()
    config.load_incluster_config()
    app.run(debug=True, host="0.0.0.0", port=7777)
