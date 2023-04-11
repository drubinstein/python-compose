import argparse
import multiprocessing
import pathlib
from typing import List, cast

from python_compose.spec import Unit, YamlSpec
from python_compose.unit.compose_unit import ComposeUnit
from python_compose.unit.conda import CondaUnit, MambaUnit
from python_compose.unit.poetry import PoetryUnit
from python_compose.unit.pyenv_virtualenv import PyenvVirtualenvUnit
from python_compose.unit.venv import VenvUnit


def run_unit(unit: ComposeUnit, clean: bool = False) -> None:
    """Run the lifecycle of a compose unit.

    Args:
        unit: An already instantiated compose unit defining how to run the Python environment.
        clean: True to remove existing environments with the same name, else use already existing
            environments.
    """
    if clean:
        unit.clean()
    unit.create()
    unit.install_requirements()
    unit.start()


def compose(units: List[ComposeUnit], clean: bool = False) -> None:
    """Create and run all compose units.

    Args:
        units: A list of compose units to instantiate.
        clean: True to remove existing environments with the same name, else use already existing
            environments.
    """
    with multiprocessing.Pool(len(units)) as p:
        p.starmap(run_unit, ((unit, clean) for unit in units))


def from_yaml(yaml_path: pathlib.Path) -> List[Unit]:
    """Deserialize and convert the contents of a YAML file to Pydantic models.

    Args:
        yaml_path: Path to the file containing the YAML configuration.

    Returns:
        A list of Pydantic Unit models to run specified by the YAML configuration.
    """
    return cast(YamlSpec, YamlSpec.parse_file(yaml_path)).units


def pydantic_to_units(units: List[Unit]) -> List[ComposeUnit]:
    """Convert Pydantic Unit models to a list of compose units.

    Args:
        units: The Pydantic Unit models.

    Raises:
        ValueError: If the YAML file specifies a Unit that we do not support yet.

    Returns:
        A list of (internal) compose units to run.
    """
    ret: List[ComposeUnit] = []
    for unit in units:
        kwargs = {k: v for k, v in unit.dict().items() if k != "unit_type"}
        if unit.unit_type == "conda":
            ret.append(CondaUnit(**kwargs))
        elif unit.unit_type == "mamba":
            ret.append(MambaUnit(**kwargs))
        elif unit.unit_type == "poetry":
            ret.append(PoetryUnit(**kwargs))
        elif unit.unit_type == "pyenv-virtualenv":
            ret.append(PyenvVirtualenvUnit(**kwargs))
        elif unit.unit_type == "venv":
            ret.append(VenvUnit(**kwargs))
        else:
            raise ValueError(f"Invalid unit type {unit.unit_type} passed!")
    return ret


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config_path", type=pathlib.Path)
    args = parser.parse_args()

    if cast(pathlib.Path, args.config_path).suffix in [".yml", ".yaml"]:
        parsed_units = from_yaml(args.config_path)
        units = pydantic_to_units(parsed_units)
        compose(units=units)
    else:
        raise ValueError("Invalid config type passed. Currently, only yaml is supported.")


if __name__ == "__main__":
    main()
