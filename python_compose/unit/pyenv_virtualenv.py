import os
import pathlib
import shutil
import subprocess
import warnings
from typing import List, Union

from python_compose.unit.compose_unit import ComposeUnit


class PyenvVirtualenvUnit(ComposeUnit):
    """A Compose Unit for creating a pyenv virtual environment and running scripts in them."""

    def __init__(
        self,
        name: str,
        py_version: str,
        requirements: Union[pathlib.Path, List[str]],
        script_path: pathlib.Path,
        script_args: List[str],
    ):
        """

        Args:
            name: Name of the virtual environment to create.
            py_version: Python version to run the script in e.g. 3.10.
            requirements: Either a path to a requirements.txt file or a list of requirements to
                install.
            script_path: Path to the Python script to run.
            script_args: Arguments to pass to the Python script.
        """
        self.name = name
        self.py_version = py_version
        self.requirements = requirements
        self.script_path = script_path
        self.script_args = script_args

    def create(self) -> None:
        """Function for creating a virtual environment."""
        self.pyenv_root = pathlib.Path(subprocess.check_output(["pyenv", "root"]).decode().strip())
        self.env_path = self.pyenv_root / "versions" / self.name
        self.python_path = self.pyenv_root / "versions" / self.name / "bin" / "python"

        subprocess.check_call(["pyenv", "install", self.py_version, "--skip-existing"])
        if os.path.exists(self.env_path):
            warnings.warn(f"Skipping pyenv venv creation for {self.name}. Venv already exists.")
        else:
            subprocess.check_call(["pyenv", "virtualenv", self.py_version, self.name])

    def install_requirements(self) -> None:
        """Function to install any and all requirements for running a script in the virtual
        environment."""
        subprocess.check_call([str(self.python_path), "-m", "pip", "install", "-U", "pip"])
        if isinstance(self.requirements, list) and self.requirements:
            subprocess.check_call(
                [str(self.python_path), "-m", "pip", "install"] + self.requirements
            )
        elif isinstance(self.requirements, pathlib.Path):
            subprocess.check_call(
                [str(self.python_path), "-m", "pip", "install", "-r", str(self.requirements)]
            )

    def start(self) -> None:
        """Function to start a script in the previously created virtual environment"""
        p = subprocess.Popen([str(self.python_path), str(self.script_path)] + self.script_args)
        p.communicate()

    def clean(self) -> None:
        """Function to erase any pre-existing files to be recreated by a Python Compose Unit."""
        shutil.rmtree(self.env_path)
