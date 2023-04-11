import pathlib
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field
from pydantic_yaml import YamlModelMixin
from typing_extensions import Annotated


# TODO: Add classmethods to convert these to their a
# TODO: Move models to the associated unit class
class AnacondaUnitModelMixin(BaseModel):
    """The definition for running an Anaconda-compatible Unit."""

    name: str
    """The name of the environment."""
    requirements: Union[pathlib.Path, List[str]] = []
    """Either a path to a requirements.txt file or a list of requirements to install."""
    command: List[str]
    """A list of strings representing the command to be run."""
    working_dir: Optional[str] = None
    """The optional working directory for the script being run."""


class CondaUnitModel(AnacondaUnitModelMixin):
    """The definition for running a conda Unit."""

    unit_type: Literal["conda"]
    """Definition that this is a conda model."""


class MambaUnitModel(AnacondaUnitModelMixin):
    """The definition for running a mamba Unit."""

    unit_type: Literal["mamba"]
    """Definition that this is a mamba model."""


class PoetryUnitModel(BaseModel):
    """The definition for running a poetry Unit."""

    unit_type: Literal["poetry"]
    """Definition that this is a poetry model."""
    source_dir: str
    """Path to the top level directory for the module using poetry."""
    script_path: pathlib.Path
    """The path to a Python script to run relative to source dir."""
    script_args: List[str]
    """Arguments to pass to script_path."""


class PyenvVirtualenvUnitModel(BaseModel):
    """The definition for running a pyenv Unit."""

    unit_type: Literal["pyenv-virtualenv"]
    """Definition that this is a pyenv model."""
    name: str
    """The name of the virtual environment."""
    py_version: str
    """The base Python version to run e.g. 3.10"""
    requirements: Union[pathlib.Path, List[str]] = []
    """Either a path to a requirements.txt file or a list of requirements to install."""
    script_path: pathlib.Path
    """The path to a Python script to run."""
    script_args: List[str]
    """Arguments to pass to script_path."""


class VenvUnitModel(BaseModel):
    """The definition for running a venv Unit."""

    unit_type: Literal["venv"]
    """Definition that this is a venv model."""
    name: str
    """The name of the virtual environment."""
    env_dir: pathlib.Path
    """Location to create and save the virtual environment."""
    requirements: Union[pathlib.Path, List[str]] = []
    """Either a path to a requirements.txt file or a list of requirements to install."""
    script_path: pathlib.Path
    """The path to a Python script to run."""
    script_args: List[str]
    """Arguments to pass to script_path."""


Unit = Annotated[
    Union[
        CondaUnitModel, MambaUnitModel, PoetryUnitModel, PyenvVirtualenvUnitModel, VenvUnitModel
    ],
    Field(discriminator="unit_type"),
]
"""The collection of Unit models that we will be able to deserialize."""


# We have this class be separate from the yaml model so we can support
# toml, json, etc.
class Spec(BaseModel):
    """The definition of the Python Compose file specification."""

    units: List[Unit]
    """A list of units that will be ran through Python Compose"""


class YamlSpec(YamlModelMixin, Spec):
    """A wrapper around Spec for YAML support."""

    pass
