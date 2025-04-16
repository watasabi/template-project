from azureml.core import Environment, Workspace
from azureml.core.environment import CondaDependencies
import os

def build_env(env_name:str, conda_dependencies_file_path:str):

    # Load environment variables from .env file or release Environment variables
    SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
    RESOURCE_GROUP = os.getenv("RESOURCE_GROUP")
    WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")

    workspace = Workspace(SUBSCRIPTION_ID, RESOURCE_GROUP, WORKSPACE_NAME)

    # ws = Workspace.from_config()

    conda_dep = CondaDependencies(conda_dependencies_file_path=conda_dependencies_file_path)
    env = Environment(name=env_name)
    env.python.user_managed_dependencies = False  # Let Azure ML manage dependencies
    env.docker.enabled = True
    env.python.conda_dependencies = conda_dep

    env_var = {
        "APPSERVER": "",
        "APPDB": "",
        "APPUID": "",
        "APPPWD": "",
    }

    env.environment_variables = env_var

    # NOTE ubuntu recent version
    dockerfile = r"""
FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04
"""

    env.docker.base_dockerfile = dockerfile
    env.register(workspace)
    build = env.build(workspace)
    build.wait_for_completion(show_output=True)
    print("O Build do environment foi concluido com sucesso")