# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}

## Setup

Start the project with environment setup and run the jupyterlab

```
pip install virtualenv
virtualenv {{cookiecutter.venv_name}}
source {{cookiecutter.venv_name}}/bin/activate
pip install -r requirements.txt
jupyter lab
```
or run this script for windows users
```
pip install virtualenv
virtualenv {{cookiecutter.venv_name}}
.\{{cookiecutter.venv_name}}\Scripts\activate
pip install -r requirements.txt
jupyter lab
```
additional command to add kernel to jupyter
```
ipython kernel install --name [env-name] --user
```

## Structure

```
    |--artifacts
    |--data
        |--raw
        |--interim
        |--processed
        |--externals
    |--notebooks
    |--queries
    |--reports
        |--figures
    |--src
```


