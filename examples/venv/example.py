import pathlib

from python_compose import compose
from python_compose.unit.venv import VenvUnit

compose.compose(
    [
        VenvUnit(
            f"httpd_{i}",
            pathlib.Path("./.envs"),
            [],
            pathlib.Path("./httpd.py"),
            [str(8080 + i)],
        )
        for i in range(3)
    ]
)
