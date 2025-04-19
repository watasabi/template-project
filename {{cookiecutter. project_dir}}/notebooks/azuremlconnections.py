from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import Dataset
from collections.abc import Mapping, Iterable

WORKSPACE_NAME = ""
RESOURCE_GROUP = ""
SUBSCRIPTION_ID = ""

ws = Workspace(
    subscription_id=SUBSCRIPTION_ID,
    resource_group=RESOURCE_GROUP,
    workspace_name=WORKSPACE_NAME,
)
env = ws.environments.get("mlops-example-pipeline")
pip_packages_list_registered_env = list(env.python.conda_dependencies.pip_packages)
conda_packages_list_registered_env = list(env.python.conda_dependencies.conda_packages)

from azureml.core.environment import CondaDependencies

# extract CondaDependecies from file
conda_dep = CondaDependencies(
    conda_dependencies_file_path="../src/config/pipe_env/env.yml"
)
eva_conda = conda_dep.__dict__
eva_conda = eva_conda["_conda_dependencies"]

# extract CondaDependecies from registered Environment
conda_dep_registered_env = env.__dict__
conda_dep_registered_env = conda_dep_registered_env["python"].__dict__
conda_dep_registered_env = conda_dep_registered_env["conda_dependencies"].__dict__
conda_dep_registered_env = conda_dep_registered_env["_conda_dependencies"] 


def normalize_conda_dependencies(conda_dependencies):
    """
    Normaliza as estruturas de CondaDependencies para comparação.
    - Garante que as listas sejam ordenadas.
    - Converte OrderedDicts e dicionários aninhados em dicionários simples.
    """
    def normalize(value):
        if isinstance(value, Mapping):  # Normaliza dicionários
            return {k: normalize(v) for k, v in sorted(value.items(), key=lambda item: item[0])}
        elif isinstance(value, list):  # Ordena listas
            return sorted(normalize(v) for v in value if not isinstance(v, dict)) + \
                   [normalize(v) for v in value if isinstance(v, dict)]
        elif isinstance(value, tuple):  # Converte tuplas em listas ordenadas
            return sorted(normalize(v) for v in value)
        else:
            return value  # Retorna o valor diretamente se não for iterável

    return normalize(conda_dependencies)

normalized_registered_env = normalize_conda_dependencies(conda_dep_registered_env)
normalized_eva_conda = normalize_conda_dependencies(eva_conda)