import pathlib
import subprocess
import warnings
from typing import List, Optional, Union

from python_compose.unit.compose_unit import ComposeUnit


class AnacondaUnit(ComposeUnit):
    """A base Compose Unit for creating anaconda-compatible environments and
    running scripts in them."""

    EXECUTABLE_NAME = ""

    def __init__(
        self,
        name: str,
        requirements: Union[pathlib.Path, List[str]],
        command: List[str],
        working_dir: Optional[pathlib.Path] = None,
    ):
        """

        Args:
            name: Name of the environment to create.
            requirements: Either a path to a requirements.txt file or a list of requirements to
                install.
            command: The command to run in the environment
            working_dir: The optional working directory for the command being run.
        """
        self.name = name
        self.requirements = requirements
        self.command = command
        self.working_dir = working_dir

    def create(self) -> None:
        """Function for creating a virtual environment."""
        envs = [
            row.split()[0]
            for row in subprocess.check_output([self.EXECUTABLE_NAME, "env", "list"])
            .decode()
            .split("\n")[2:]
            if row
        ]
        if self.name in envs:
            warnings.warn(f"Skipping pyenv venv creation for {self.name}. Venv already exists.")
        else:
            subprocess.check_call([self.EXECUTABLE_NAME, "create", "-n", self.name, "-y"])

    def install_requirements(self) -> None:
        """Function to install any and all requirements for running a script in the virtual
        environment."""
        if isinstance(self.requirements, list) and self.requirements:
            subprocess.check_call(
                [self.EXECUTABLE_NAME, "install", "-n", self.name] + self.requirements
            )
        elif isinstance(self.requirements, pathlib.Path):
            subprocess.check_call(
                [self.EXECUTABLE_NAME, "install", "-n", self.name, "-f", str(self.requirements)]
            )

    def start(self) -> None:
        """Function to start a script in the previously created virtual environment."""
        p = subprocess.Popen(
            [self.EXECUTABLE_NAME, "run", "-n", self.name, "--no-capture-output"]
            + (["--cwd", str(self.working_dir)] if self.working_dir else [])
            + self.command
        )
        p.communicate()

    def clean(self) -> None:
        """Function to erase any pre-existing files to be recreated by a Python Compose Unit."""
        subprocess.check_call([self.EXECUTABLE_NAME, "remove", "-n", self.name, "--all"])


class CondaUnit(AnacondaUnit):
    """A Compose Unit for creating conda environments and running scripts in them."""

    EXECUTABLE_NAME = "conda"


class MambaUnit(AnacondaUnit):
    """A Compose Unit for creating mamba environments and running scripts in them."""

    EXECUTABLE_NAME = "mamba"
