import pathlib

from python_compose import compose
from python_compose.unit.pyenv_virtualenv import PyenvVirtualenvUnit

compose.compose(
    [
        PyenvVirtualenvUnit(
            name=f"httpd_{i}",
            py_version=f"3.{9+i}",
            requirements=[],
            script_path=pathlib.Path("./httpd.py"),
            script_args=[str(8080 + i)],
        )
        for i in range(3)
    ]
)
