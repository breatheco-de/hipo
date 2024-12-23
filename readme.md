# Hypo Project

This project aims to serve as a server that processes pipelines using Prefect, stores temporal memory to use for AI Agents and serves as a REST API to retrieve the results of the pipelines.

## How to run the project

1. Init a virtual environment

```
python -m venv venv
```

2. Activate the virtual environment

```
.\venv\Scripts\activate
```

3. Install the dependencies with `pip install -r requirements.txt`

4. Run the project with `prefect server start`

5. Start a work pool

```
prefect work-pool start my-work-pool
```

## How to add a new pipeline

1. Create a new folder in the src/pipelines folder with the name of the pipeline.
2. Create a new python file named run.py in the folder and add the code for the pipeline. It must contain at least a function decorated with @flow.
3. In the root/prefect.yaml file, add a new deployment for the pipeline.
4. Run the command `prefect deploy` to deploy the pipeline.
