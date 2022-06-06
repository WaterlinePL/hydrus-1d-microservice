# Job management microservice

This is a repository of a microservice that launches Kubernetes Jobs related to simulation flow. Jobs present in flow:
* [Project download](https://github.com/WaterlinePL/project-download-job) - download project files in order to launch simulations
* [Hydrus simulation](https://github.com/WaterlinePL/hydrus-job) - launch Hydrus simulation
* (Data transfer) (TODO) - transfer data from Hydrus to Modflow
* [Modflow simulation](https://github.com/WaterlinePL/modflow-job) - launch Modflow simulation
* Cleanup (TODO) - upload simulation output and delete files from temporary volume
