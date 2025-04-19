# Data Project Template

## Author
- [Rodrigo Watanabe Pisaia]

## Getting Started
To get started with this project you need to:
```bash
pip install uv
uvx cookiecutter https://github.com/watasabi/template-project
```

## Project Organization
```
.
├── LICENCE
├── README.md
├── data
│   ├── external
│   ├── interim
│   ├── processed
│   └── raw
├── models
├── notebooks
│   ├── azuremlconnections.py
│   └── general.py
├── pipe
│   ├── __pycache__
│   │   └── azureml_env_build.cpython-310.pyc
│   ├── azureml_env_build.py
│   ├── azureml_pipe_orchestrator.py
│   └── utils
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-310.pyc
│       │   └── compare_env_version.cpython-310.pyc
│       └── compare_env_version.py
├── references
├── release
│   └── release_template.json
├── reports
│   └── figures
├── requirements.txt
└── src
    ├── 01_load_data.py
    ├── 02_preprocessing.py
    ├── 03_model_inference.py
    ├── 04_post_processing.py
    ├── __init__.py
    ├── config
    │   └── pipe_env
    │       └── env.yml
    ├── modeling
    │   └── __init__.py
    ├── services
    │   └── __init__.py
    └── utils
```