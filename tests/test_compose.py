import os
import pathlib
import platform
import random
import shutil
import string
from collections import Counter

import pytest

from python_compose import compose
from python_compose.unit.conda import CondaUnit
from python_compose.unit.pyenv_virtualenv import PyenvVirtualenvUnit
from python_compose.unit.venv import VenvUnit


@pytest.fixture(autouse=True)
def random_string() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=100))


def test_venv(tmp_path: pathlib.Path, random_string: str) -> None:
    output_file = tmp_path / "0.txt"
    compose.compose(
        [
            VenvUnit(
                "test",
                tmp_path,
                [],
                pathlib.Path("tests") / "create_file.py",
                [str(output_file), random_string],
            )
        ]
    )
    with open(output_file) as f:
        assert f.read() == random_string


@pytest.mark.skipif(shutil.which("pyenv") is None, reason="pyenv is not installed on the system.")
def test_pyenv(tmp_path: pathlib.Path, random_string: str) -> None:
    output_file = tmp_path / "0.txt"
    compose.compose(
        [
            PyenvVirtualenvUnit(
                "test",
                "3.9",
                [],
                pathlib.Path("tests") / "create_file.py",
                [str(output_file), random_string],
            )
        ]
    )
    with open(output_file) as f:
        assert f.read() == random_string


@pytest.mark.skipif(shutil.which("conda") is None, reason="conda is not installed on the system.")
def test_conda(tmp_path: pathlib.Path, random_string: str) -> None:
    output_file = tmp_path / "0.txt"
    compose.compose(
        [
            CondaUnit(
                "test",
                [],
                [
                    "python3",
                    os.path.join("tests", "create_file.py"),
                    str(output_file),
                    random_string,
                ],
            )
        ]
    )
    with open(output_file) as f:
        assert f.read() == random_string


def test_yaml_deserialization() -> None:
    units = compose.from_yaml(pathlib.Path("tests") / "config.yaml")
    assert len(units) == 3
    counter: Counter[str] = Counter()
    for unit in units:
        counter[unit.unit_type] += 1
    assert counter["venv"] == 1 and counter["pyenv-virtualenv"] == 1 and counter["conda"] == 1


def test_pydantic_to_compose_unit() -> None:
    units = compose.pydantic_to_units(
        compose.from_yaml(pathlib.Path("tests") / "config.yaml"))
    assert len(units) == 3
    counter: Counter[str] = Counter()
    for unit in units:
        counter[type(unit).__name__] += 1
    print(counter)
    assert (
        counter["VenvUnit"] == 1
        and counter["PyenvVirtualenvUnit"] == 1
        and counter["CondaUnit"] == 1
    )
