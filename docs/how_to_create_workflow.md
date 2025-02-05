# How to create a workflow with Prefect

### 1. Create a new directory inside `src/pipelines` directory

You may see the `src` directory as the root of the project. Inside the `src` directory, you can find the `pipelines` directory. Inside the `pipelines` directory, the first step to creat a workflow is create another directory inside `src/pipelines` directory.

### 2. Create a new file inside the new directory called `run.py`

The file should have this structure to be recognized as a Prefect workflow:

```python
from prefect import task, flow

@task # This is a task that will be executed in some point of the workflow
def mi_tarea():
    print("¡Tarea ejecutada!")

@flow # This is the main function that will be executed when the workflow is run
def hello_world():
    mi_tarea()

if __name__ == "__main__":
    hello_world()

```

### 3. Add the deployment in the `prefect.yaml` file

The `prefect.yaml` file is the file that contains the configuration for the Prefect project. You can find it in the root of the project. Inside the deployments section, you can add the deployment for the new workflow. This is an example of a working deployment:

##### Lets understand the important keys:

- `name`: The name of the deployment.
- `entrypoint`: The path to the file that contains the workflow separated by `:` of the decorated function with the `@flow` decorator. For example: `src/pipelines/create_live_documents/run.py:create_live_documents_flow`

- `work_pool`: The name of the work pool to use for the deployment. Live this as the rest to avoid extra configuration.
- `schedules`: A list of schedules to run the workflow, including the interval in seconds and the anchor date. (You can ask an AI to generate a deployment based in this documentation)

```yaml
- name: create-live-documents
  version:
  tags: []
  description:
  entrypoint: src/pipelines/create_live_documents/run.py:create_live_documents_flow
  parameters: {}
  work_pool:
    name: my-work-pool
    work_queue_name:
    job_variables: {}
  concurrency_limit:
  enforce_parameter_schema: true
  schedules:
    - interval: 86400.0
      anchor_date: "2024-12-23T10:27:34.959684+00:00"
      timezone: UTC
      active: true
```

### 4. Deploy the workflows

To deploy the workflows, you can use the following command:

```bash
prefect deploy
```

This command will take the prefect.yaml file and deploy the workflows to the Prefect instance locally.

### 5. Run the workflow

After running the previous step, prefect will give you the command to run inmediately the workflow.

### 6. Check the logs

Check the console or the prefect UI and verify that the deployment was created successfully and is up and running.
