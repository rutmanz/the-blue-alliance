from _pytest import python as python, unittest as unittest
from _pytest.config import hookimpl as hookimpl
from typing import Any

def pytest_runtest_setup(item: Any): ...
def teardown_nose(item: Any) -> None: ...
def is_potential_nosetest(item: Any): ...
def call_optional(obj: Any, name: Any): ...