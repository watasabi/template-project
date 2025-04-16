from azureml.pipeline.steps import PythonScriptStep
from azureml.core.compute_target import ComputeTargetException
from azureml.data.datapath import DataPath, DataPathComputeBinding
from azure.core.credentials import AzureSasCredential
from azureml.pipeline.core import (
    Pipeline,
    StepSequence,
    PipelineData,
    PipelineEndpoint,
)
from azureml.core import (
    Workspace,
    Experiment,
    Environment,
    ComputeTarget,
    RunConfiguration,
    Datastore,
)
from azureml.core.environment import CondaDependencies
from utils import normalize_conda_dependencies
from azureml_env_build import build_env
import os
import glob

print("Loading workspace")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP")
WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")
COMPUTE_CLUSTER = os.getenv("COMPUTE_CLUSTER")
ws = Workspace(SUBSCRIPTION_ID, RESOURCE_GROUP, WORKSPACE_NAME)
print("Loading experiment")
experiment = Experiment(workspace=ws, name="pipeline_example")
datastore = Datastore.get_default(ws)

## access compute cluster
try:
    compute_target = ComputeTarget(
        workspace=ws,
        name=COMPUTE_CLUSTER,
    )
    print("Found existing compute target")
except ComputeTargetException:
    compute_target = None
    print("Compute target not found")

## setup environment
env_name = "mlops-example-pipeline-env3"
conda_dependencies_file_path = "./src/config/pipe_env/env.yml"

if compute_target is not None:
    compute_target.wait_for_completion(show_output=True)
    try:
        env = Environment.get(workspace=ws, name=env_name)
        conda_dep_env = (
            env.__dict__["python"]
            .__dict__["conda_dependencies"]
            .__dict__["_conda_dependencies"]
        )
        conda_dep_file = CondaDependencies(
            conda_dependencies_file_path=conda_dependencies_file_path
        )
        if normalize_conda_dependencies(conda_dep_env) == normalize_conda_dependencies(
            conda_dep_file.__dict__["_conda_dependencies"]
        ):
            print("Environment is up to date")
            pass
        else:
            print("Updating environment")
            env.python.conda_dependencies = conda_dep_file
            env.register(workspace=ws)
            env = Environment.get(workspace=ws, name=env_name)
            print("Environment updated")
    except Exception:
        print("Environment not found. Creating a new one.")
        print("Building environment...")

        build_env(env_name=env_name, conda_dependencies_file_path=conda_dependencies_file_path)
        env = Environment.get(workspace=ws, name=env_name)
        print("Environment build completed")


    run = RunConfiguration()
    run.environment = env
    run.target = compute_target


source_directory = "./src"
data_raw = PipelineData(
    "data_raw", datastore=datastore, output_path_on_compute="azureml/"
)
data_transformed = PipelineData(
    "data_transformed", datastore=datastore, output_path_on_compute="azureml/"
)
data_inference = PipelineData(
    "data_inference", datastore=datastore, output_path_on_compute="azureml/"
)
transform_pipeline = PipelineData(
    "transform_pipeline", datastore=datastore, output_path_on_compute="azureml/"
)


## pipeline step sequences
pipe_step1 = PythonScriptStep(
    name="Load raw dataset",
    script_name="01_load_data.py",
    arguments=[
        "--data_raw",
        data_raw,
    ],
    outputs=[data_raw],
    compute_target=compute_target,
    runconfig=run,
    source_directory=source_directory,
    allow_reuse=False,
)

pipe_step2 = PythonScriptStep(
    name="Preprocess data",
    script_name="02_preprocessing.py",
    arguments=[
        "--data_raw",
        data_raw,
        "--data_transformed",
        data_transformed,
        "--transform_pipeline",
        transform_pipeline,
    ],
    inputs=[data_raw],
    outputs=[data_transformed, transform_pipeline],
    compute_target=compute_target,
    runconfig=run,
    source_directory=source_directory,
    allow_reuse=False,
)
pipe_step3 = PythonScriptStep(
    name="Model Inference",
    script_name="03_model_inference.py",
    arguments=[
        "--data_transformed",
        data_transformed,
        "--data_inference",
        data_inference,
    ],
    inputs=[data_transformed],
    outputs=[data_inference],
    runconfig=run,
    compute_target=compute_target,
    source_directory=source_directory,
    allow_reuse=False,
)

pipe_step4 = PythonScriptStep(
    name="Post Processing",
    script_name="04_post_processing.py",
    arguments=[
        "--data_inference",
        data_inference,
        "--transform_pipeline",
        transform_pipeline,
        "--raw_data",
        data_raw,
    ],
    inputs=[data_inference, transform_pipeline, data_raw],
    runconfig=run,
    compute_target=compute_target,
    source_directory=source_directory,
    allow_reuse=False,
)

step_sequence = [pipe_step1, pipe_step2, pipe_step3, pipe_step4]
pipeline = Pipeline(
    workspace=ws, steps=step_sequence, description="pipeline example steps"
)
print("Pipeline is built.")

pipeline_run = experiment.submit(pipeline, regenerate_outputs=True)
pipeline_run.wait_for_completion(show_output=True)


if __name__ == "__main__":
    RUN = True  # TODO change this if you want to run the pipeline
    DEPLOY = True  # TODO change this if you want to deploy the pipeline
    description = "Publish pipeline example"
    if RUN:
        # Submitting the run
        pipeline_run = experiment.submit(
            pipeline,
            regenerate_outputs=True,
        )
        pipeline_run.wait_for_completion(show_output=False)

    if DEPLOY:
        # Check if the pipeline endpoint exists
        try:
            pipeline_endpoint_by_name = PipelineEndpoint.get(
                workspace=ws, name="pipeline_example"
            )
            print("Pipeline Endpoint found")
        except Exception as e:
            if "PipelineEndpoint name pipeline_example not found" not in str(e):
                raise e

            print("Pipeline Endpoint not found. Creating a new one.")
            published = pipeline.publish(
                name="pipeline_example",
                description=description,
            )
            pipeline_endpoint_by_name = PipelineEndpoint.publish(
                workspace=ws,
                name="pipeline_example_endpoint",
                pipeline=published,
                description=description,
            )

        # Add the latest version of the pipeline to the endpoint
        published = pipeline.publish(
            name="pipeline_example_endpoint",
            description=description,
        )
        pipeline_endpoint_by_name.add(published)

        # Setting the latest version as default
        pipeline_endpoint_by_name.set_default_version(
            pipeline_endpoint_by_name.list_versions()[-1].version
        )
