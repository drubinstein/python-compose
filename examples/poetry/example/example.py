import os
import pathlib

from python_compose import compose
from python_compose.unit.poetry import PoetryUnit

compose.compose(
    [
        PoetryUnit(
            pathlib.Path(os.path.dirname(os.path.dirname(__file__))),
            pathlib.Path(os.path.join(os.path.dirname(__file__), "httpd.py")),
            ["8080"],
        )
    ]
)
