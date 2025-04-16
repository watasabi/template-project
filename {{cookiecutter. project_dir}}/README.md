<a id="readme-top"></a>
<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#{{ cookiecutter.project_name.lower().replace(' ', '-').replace('_', '-') }}">{{ cookiecutter.project_name }}</a>
    </li>
    <li><a href="#author">Author</a></li>
    <li><a href="#key-users">Key Users</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#setup-environment">Setup Environment</a></li>
        <li><a href="#running">Running</a></li>
      </ul>
    </li>
    <li><a href="#key-users">Key Users</a></li>
    <li><a href="#azureml-infos">AzureML Infos</a></li>
    <li><a href="#data">Data</a></li>
    <li><a href="#datafactory-pipeline">DataFactory Pipeline</a></li>
    <li><a href="#structure">Structure</a></li>
  </ol>
</details>


# {{ cookiecutter.project_name }}

{{ cookiecutter.project_desc }}

## Adjusting .gitignore


Ensure you adjust the `.gitignore` file according to your project needs. For example, since this is a template, the `/data/` folder is commented out and data will not be exlucded from source control:

```plaintext
# exclude data from source control by default
# /data/
```

Typically, you want to exclude this folder if it contains either sensitive data that you do not want to add to version control or large files.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Author

- [{{ cookiecutter.full_name }}]({{ cookiecutter.email }})


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Key Users

- [Nome](email)
- [Nome](email)
- [Nome](email)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### AzureML Infos
```
Workspace: **TODO** 
Job Pipeline: **TODO** 
Custom Environment: **TODO** 
Pipeline Endpoint: **TODO** 
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Data

```
**TODO**
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### DataFactory Pipeline
```
**TODO**
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Structure

```
├── LICENSE            <- Open-source license if one is chosen
├── README.md          <- The top-level README for developers using this project
├── data
│   ├── external       <- Data from third party sources
│   ├── interim        <- Intermediate data that has been transformed
│   ├── processed      <- The final, canonical data sets for modeling
│   └── raw            <- The original, immutable data dump
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── src                         <- Source code for this project
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    │    
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    ├── plots.py                <- Code to create visualizations 
    │
    └── services                <- Service classes to connect with external platforms, tools, or APIs
        └── __init__.py 
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


