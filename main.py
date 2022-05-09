from flask import Flask, request
from strenum import StrEnum

import kubernetes_job_operator
from job_generator.yaml_data import HydrologicalModelEnum

app = Flask(__name__)


class RestMethod(StrEnum):
    GET = 'GET'
    DELETE = 'DELETE'
    PUT = 'PUT'
    POST = 'POST'


@app.route("/hydrus", methods=[RestMethod.GET, RestMethod.POST])
def manage_hydrus():
    if request.method == RestMethod.GET:
        kubernetes_job_operator.get_job_status(request.json["job_name"], HydrologicalModelEnum.HYDRUS)
    elif request.method == RestMethod.POST:
        project_name = request.json["project_name"]
        model_name = request.json["model_name"]
        kubernetes_job_operator.create_job(project_name, model_name, HydrologicalModelEnum.HYDRUS)


if __name__ == '__main__':
    # run flask app
    app.run(debug=True, host="0.0.0.0", port=7777)
