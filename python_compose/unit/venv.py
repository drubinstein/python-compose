import pathlib
import shutil
import subprocess
import venv
from typing import List, Union

from python_compose.unit.compose_unit import ComposeUnit


class VenvUnit(ComposeUnit):
    """A Compose Unit for creating a venv virtual environment and running scripts in it."""

    def __init__(
        self,
        name: str,
        env_dir: pathlib.Path,
        requirements: Union[pathlib.Path, List[str]],
        script_path: pathlib.Path,
        script_args: List[str],
    ):
        """

        Args:
            name: Name of the virtual environment to create.
            env_dir: Directory to create and save the venv.
            requirements: Either a path to a requirements.txt file or a list of requirements to
                install.
            script_path: Path to the Python script to run.
            script_args: Arguments to pass to the Python script.
        """
        self.name = name
        self.env_dir = env_dir
        self.env_path = self.env_dir / self.name
        self.python_path = self.env_path / "bin" / "python"
        self.requirements = requirements
        self.script_path = script_path
        self.script_args = script_args

    def create(self) -> None:
        """Function for creating a virtual environment."""
        venv.create(self.env_path, system_site_packages=True, clear=False, with_pip=True)  # type: ignore[attr-defined] # noqa

    def install_requirements(self) -> None:
        """Function to install any and all requirements for running a script in the virtual
        environment."""
        if isinstance(self.requirements, list) and self.requirements:
            subprocess.check_call(
                [str(self.python_path), "-m", "pip", "install"] + self.requirements
            )
        elif isinstance(self.requirements, pathlib.Path):
            subprocess.check_call(
                [str(self.python_path), "-m", "pip", "install", "-r", str(self.requirements)]
            )

    def start(self) -> None:
        """Function to start a script in the previously created virtual environment."""
        p = subprocess.Popen([str(self.python_path), str(self.script_path)] + self.script_args)
        p.communicate()

    def clean(self) -> None:
        """Function to erase any pre-existing files to: be recreated by a Python Compose Unit."""
        shutil.rmtree(self.env_path)
