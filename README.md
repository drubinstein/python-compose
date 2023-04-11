# Python Compose

![License](https://img.shields.io/badge/license-MIT-blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-compose)
![Supported Platforms](https://img.shields.io/badge/platforms-macOS%20%7C%20Linux-green)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/python-compose)](https://pypistats.org/packages/python-compose)
[![GitHub Repo stars](https://img.shields.io/github/stars/drubinstein/python-compose?style=social)](https://github.com/drubinstein/python-compose/stargazers)


Python Compose is a command line tool and library for spinning up many long-running python applications in _isolated Python environments_. Inspired by [Docker Compose](https://docs.docker.com/compose/), Python Compose is meant to provide similar functionality without having to relying on Docker containers, networking etc.

Currently, Python Compose supports the following environments:
- [conda](https://docs.conda.io/en/latest/)
- [mamba](https://mamba.readthedocs.io/en/latest/index.html)
- [poetry](https://python-poetry.org/)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
- [venv](https://docs.python.org/3/library/venv.html)

In the future, we wish to support:

- [pipenv](https://pipenv.pypa.io/en/latest/)
- [pyenv](https://github.com/pyenv/pyenv)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `python-compose`.

```bash
pip install python-compose
```

Currently, Python Compose supports `venv`, `pyenv-virtualenv` and `conda` environments. The `pyenv-virtualenv` and `conda` managers are not installed with Python Compose. To install them, follow instructions from the [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) and [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) documentation.

## Concepts

### Unit
A `unit` is an object which represents how to create, run and clean up a service for a specific type of Python environment handler. Examples can be found in the [python_compose/unit](python_compose/unit/) directory.

### YAML Specification

Python Compile can currently only be instantiated from a YAML file with specification derived from the internal [spec.py](python_compose/spec.py) Python file. A Python Compose YAML file expects a top-level key, `units` which maps to a list of `units` i.e. Python scripts to run. Each unit's environment is described by the key `unit_type`. A unit will have different arguments. Some required, some are optional. Again, these definitions are in [spec.py](python_compose/spec.py)

## Alternatives Comparison

Python Compose isn't the only tool in the world for this task. It happens to be a convenient one if you're working in a Python only environment and want to minimize external tools and dependencies. Below is a chart comparing Python Compose versus other solutions.

|        **Tool**        | **Operating Systems** | **Virtual Networking** |                **Ability to Run Non-Python Programs**                | **Multiple Python Version Support** | **Non-Python Dependencies Required** |
|:----------------------:|:---------------------:|:----------------------:|:-----------------------------------------------------------------------------:|:-----------------------------------:|:------------------------------------:|
|     Python Compose     |  Linux/MacOS  |            ❌           | With Conda or [subprocess](https://docs.python.org/3/library/subprocess.html) |                  ✅                  |                   ❌                  |
| Python Multiprocessing |  Linux/MacOS/Windows  |            ❌           |      With [subprocess](https://docs.python.org/3/library/subprocess.html)     |                  ❌                  |                   ❌                  |
|     Docker Compose     |  Linux/MacOS/Windows  |            ✅           |                                       ✅                                       |                  ✅                  |                   ✅                  |
|   Systemd Unit Files   |         Linux         |            ❌           |                                       ✅                                       |                  ✅                  |                   ✅                  |
|   Bazel    |         Linux/MacOS/Windows         |            ❌           |                                       ✅                                       |                  ✅                  |                   ✅                  |


## Example

We provide many examples of how to use Python Compose as both a library and as a command line tool in the `examples` directory. Below we provide what we will assume is the most Docker Compose-like use case, starting many backend services from a single config file.

In a directory, create a Python script, `httpd.py` that starts an HTTP service:

```python
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int)
    args = parser.parse_args()

    print(args)
    server_address = ("", args.port)
    httpd = HTTPServer(server_address, BaseHTTPRequestHandler)
    httpd.serve_forever()

```

Then, create a yaml file, `config.yaml` to start this backend service in multiple environments:

```yaml
units:
- unit_type: "venv"
  name: "httpd_0"
  env_dir: "./.envs"
  script_path: "./httpd.py"
  script_args: ["8080"]
- unit_type: "venv"
  name: "httpd_1"
  env_dir: "./.envs"
  script_path: "./httpd.py"
  script_args: ["8081"]
- unit_type: "pyenv-virtualenv"
  name: "httpd_2"
  py_version: "3.10"
  script_path: "./httpd.py"
  script_args: ["8082"]
- unit_type: "conda"
  name: httpd_3
  script: ["python3", "../conda/httpd.py", "8083"]
```

To spin up all containers, run

```bash
python3 -m python-compose config.yaml
```

To exit, press `<Ctrl-C>`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Setting up Your Development Environment.

Developers should first install all needed development dependencies:

```bash
pip3 install -e '.[dev]'
```

Then make all desired changes

### Adding a new Unit

To add a new `unit`, you will want to first add the unit to [python_compose/unit](python_compose/unit). Then, add an example to the examples directory and finally update [spec.py](python_compose/spec.py).

### Testing

To test Python Compile, run `pytest` after installation of all dev dependencies.

## License

[MIT](https://choosealicense.com/licenses/mit/)
