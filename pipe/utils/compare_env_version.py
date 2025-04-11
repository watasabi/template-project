from collections.abc import Mapping, Iterable

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