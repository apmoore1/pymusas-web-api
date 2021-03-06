# PyMUSAS Web API

Web API for [PyMUSAS](https://ucrel.github.io/pymusas/) built on the [FastAPI framework](https://fastapi.tiangolo.com/).

## Install

The requirements can be installed two different ways, but at the moment in both cases you need to download the repository locally:

* Python package install: `pip install .`
* Requirements file install: `pip install -r requirements.txt`

## Running the API

At the moment in both cases you need to download the repository locally, after which you can run the API in two different ways depending if you have installed it as a Python package or you have just installed the requirements:

If you have installed the package, e.g. `pip install .`, you can run the app like so (this **can** be ran outside of this repository):

``` bash
pymusas_web_api
```

Else if you have installed the requirements through the requirements file, e.g. `pip install -r requirements.txt`, you can the app like so (this **cannot** be ran outside of this repository):

``` bash
python pymusas_web_api
```

In **both** cases you can also use the following optional command line arguments:

```
Arguments to run the uvicorn server.

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Default: 127.0.0.1
  --port PORT           Default: 5000
  --log-level LOG_LEVEL Default: info
  --reload              Enable auto-reload (Default False)
```


## Development

When developing on the project you will want to install the Python package locally in editable format with all the extra requirements, this can be done like so:

``` bash
pip install -e .[tests]
```

For a zsh shell, which is the default shell for the new Macs you will need to escape with \ the brackets:

``` bash
pip install -e .\[tests\]
```

### Running linters and tests

This code base uses isort, flake8, and mypy to ensure that the format of the code is consistent and contain type hints. The flake8 settings can be found in [./setup.cfg](./setup.cfg) and the isort and mypy settings within [./pyproject.toml](./pyproject.toml). To run these linters:

``` bash
isort pymusas_web_api/ tests/
flake8
mypy
```

To run the tests with code coverage, the pytest and coverage settings can be found within [./pyproject.toml](./pyproject.toml):

``` bash
coverage run # Runs the tests (uses pytest)
coverage report # Produces a command line report on the test coverage
```

If you would like a JSON or XML code coverage report run the respective commands to produce a `coverage.json` or `coverage.xml` file respectively:

``` bash
coverage json
coverage xml
```