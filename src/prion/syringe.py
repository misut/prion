from __future__ import annotations

from typing import Any

from prion._internal.dependency import Dependency, DependencyState


class Syringe:

    def __init__(self) -> None:
        self._dependencies: dict[str, DependencyState] = {}


def single() -> Any:
    return Dependency("single")


def factory() -> Any:
    return Dependency("factory")
