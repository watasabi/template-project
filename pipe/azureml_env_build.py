from azureml.core import Environment, Workspace
from azureml.core.environment import CondaDependencies
import dotenv
import os
dotenv.load_dotenv("../src/config/.env")

SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP")
WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")

workspace = Workspace(SUBSCRIPTION_ID, RESOURCE_GROUP, WORKSPACE_NAME)

# ws = Workspace.from_config()

conda_dep = CondaDependencies(conda_dependencies_file_path="../src/config/pipe_env/env.yml")
# conda_dep.add_channel("conda-forge")
env = Environment(name="mlops-example-pipeline")
env.python.user_managed_dependencies = False  # Let Azure ML manage dependencies
env.docker.enabled = True
env.python.conda_dependencies = conda_dep

env_var = {
    "APPSERVER": "",
    "APPDB": "",
    "APPUID": "",
    "APPPWD": "",
    # "SUBSCRIPTION_ID": "21113636-9177-4577-907f-2b773e81f048",
    # "RESOURCE_GROUP": "BRF-RG-ANLTCS-IA-LAB",
    # "WORKSPACE_NAME": "brf-ml-analytics-dev",
}

env.environment_variables = env_var

# NOTE ubuntu recent version
dockerfile = r"""
FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04
"""
env.docker.base_dockerfile = dockerfile

env.register(ws)
env.build(ws)
