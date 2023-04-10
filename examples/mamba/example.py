from python_compose import compose
from python_compose.unit.conda import MambaUnit

compose.compose(
    [
        MambaUnit(
            name=f"httpd_{i}", requirements=[], command=["python3", "httpd.py", str(8080 + i)]
        )
        for i in range(3)
    ]
)
