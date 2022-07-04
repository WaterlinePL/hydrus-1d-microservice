# Job management microservice

This is a repository of a microservice that launches Kubernetes Jobs related to simulation flow. Jobs present in flow:
* [Project download](https://github.com/WaterlinePL/project-download-job) - download project files in order to launch simulations (TODO: download based on .json from MinIO)
* [Hydrus simulation](https://github.com/WaterlinePL/hydrus-job) - launch Hydrus simulation
* [Modflow simulation](https://github.com/WaterlinePL/modflow-job) - launch Modflow simulation (TODO: data transfer)
* [Cleanup](https://github.com/WaterlinePL/simulation-cleanup-job) - upload simulation output and delete files from temporary volume


## API 
Preferably body of requests should be a JSON. Responses are in JSON.

1. **POST** `/project-files`  
Request:
```json
{
  "projectId": "vytxeTZskVKR7C7WgdSP3d",
  "hydrusModels": ["model1", "model2", "model3"],
  "modflowModel": "modModel"
}
```
Returns download job ID in response. Job ID is used in order to monitor status of job downloading project files (**GET** `/status/{jobID}`).  
  
2. **POST** `/simulation/hydrus`  
Request:
```json
{
  "projectId": "vytxeTZskVKR7C7WgdSP3d",
  "modelName": "exu3DTbj2ncsn9tLdLWspw"
}
```
Returns Hydrus simulation job ID in response. Job ID is used to monitor status of Hydrus simulation (**GET** `/status/{jobID}`).  
  
3. **POST** `/simulation/modflow`  
Request:
```json
{
  "modelDetails": {
    "projectId": "vytxeTZskVKR7C7WgdSP3d",
    "modelName": "exu3DTbj2ncsn9tLdLWspw"
  },
  "spinUp": 365
}
```
Returns Modflow simulation job ID in response. Job ID is used to monitor status of Modflow simulation (**GET** `/status/{jobID}`).  
  
4. **DELETE** `/project-files/{projectId}`
Returns cleanup job ID in response. Job ID is used in order to monitor status of job cleaning temporary volume (**GET** `/status/{jobID}`).
