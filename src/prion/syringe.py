from __future__ import annotations

from typing import Any, Generic, TypeVar

from prion._internal.dependency import Dependency, DependencyState

T = TypeVar("T")


class Syringe:
    def __init__(self) -> None:
        self._dependencies: dict[str, DependencyState[Any]] = {}


class single(Dependency[T], Generic[T]):
    """Singleton dependency — provider is called once, result is cached."""

    def __init__(self) -> None:
        super().__init__("single")


class factory(Dependency[T], Generic[T]):
    """Factory dependency — provider is called on every access."""

    def __init__(self) -> None:
        super().__init__("factory")
