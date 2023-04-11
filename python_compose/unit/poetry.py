import pathlib
import shutil
import subprocess
from typing import List

from python_compose.unit.compose_unit import ComposeUnit


class PoetryUnit(ComposeUnit):
    """A Compose Unit for creating a poetry virtual environment and running scripts in it."""

    def __init__(
        self,
        source_dir: pathlib.Path,
        script_path: pathlib.Path,
        script_args: List[str],
    ):
        """

        Args:
            source_dir: Top level directory for the poetry-based module.
            script_path: Path to the Python script to run relative to source dir.
            script_args: Arguments to pass to the Python script.
        """
        self.source_dir = source_dir
        self.script_path = script_path
        self.script_args = script_args
        self.env_dir = subprocess.check_output(
            ["poetry", "env", "info", "--path"], cwd=self.source_dir
        )

    def create(self) -> None:
        """Function for creating a virtual environment."""
        # Poetry creates the virtual environments on initialization so we don't have to here.
        pass

    def install_requirements(self) -> None:
        """Function to install any and all requirements for running a script in the virtual
        environment."""
        subprocess.check_call(["poetry", "install"], cwd=self.source_dir)

    def start(self) -> None:
        """Function to start a script in the previously created virtual environment."""
        p = subprocess.Popen(
            ["poetry", "run", "python3", str(self.script_path)] + self.script_args,
            cwd=self.source_dir,
        )
        p.communicate()

    def clean(self) -> None:
        """Function to erase any pre-existing files to: be recreated by a Python Compose Unit."""
        shutil.rmtree(self.env_dir)
