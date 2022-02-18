# PyMUSAS Web API

Web API for [PyMUSAS](https://ucrel.github.io/pymusas/) built on the [FastAPI framework](https://fastapi.tiangolo.com/).

## Requirements

Tested on Python 3.9

General requirements:

``` bash
pip install -r requirements.txt
```

## Development

Development requirements:

``` bash
pip install -r dev_requirements.txt
```

### Running linters

```
isort scripts/
flake8
mypy
```