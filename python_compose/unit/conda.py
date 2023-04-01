import pathlib
import subprocess
import warnings
from typing import List, Optional, Union

from python_compose.unit.compose_unit import ComposeUnit


class CondaUnit(ComposeUnit):
    """A Compose Unit for creating Conda environments and running scripts in them."""

    def __init__(
        self,
        name: str,
        requirements: Union[pathlib.Path, List[str]],
        command: List[str],
        working_dir: Optional[pathlib.Path] = None,
    ):
        """

        Args:
            name: Name of the conda environment to create.
            requirements: Either a path to a requirements.txt file or a list of requirements to
                install.
            command: The command to run in the conda environment
            working_dir: The optional working directory for the command being run.
        """
        self.name = name
        self.requirements = requirements
        self.command = command
        self.working_dir = working_dir

    def create(self) -> None:
        """Function for creating a virtual environment."""
        conda_env_list = subprocess.check_output(
            ["conda", "env", "list"]).decode().splitlines()
        envs = []
        print(conda_env_list)
        if len(conda_env_list) >= 2:
            envs = [
                row.split()[0]
                for row in conda_env_list[2:]
                if row
            ]
        if self.name in envs:
            warnings.warn(
                f"Skipping pyenv venv creation for {self.name}. Venv already exists.")
        else:
            subprocess.check_call(["conda", "create", "-n", self.name, "-y"])

    def install_requirements(self) -> None:
        """Function to install any and all requirements for running a script in the virtual
        environment."""
        if isinstance(self.requirements, list) and self.requirements:
            subprocess.check_call(
                ["conda", "install", "-n", self.name] + self.requirements)
        elif isinstance(self.requirements, pathlib.Path):
            subprocess.check_call(
                ["conda", "install", "-n", self.name,
                    "-f", str(self.requirements)]
            )

    def start(self) -> None:
        """Function to start a script in the previously created virtual environment."""
        p = subprocess.Popen(
            ["conda", "run", "-n", self.name, "--no-capture-output"]
            + (["--cwd", str(self.working_dir)] if self.working_dir else [])
            + self.command
        )
        p.communicate()

    def clean(self) -> None:
        """Function to erase any pre-existing files to be recreated by a Python Compose Unit."""
        subprocess.check_call(["conda", "remove", "-n", self.name, "--all"])
