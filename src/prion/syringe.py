from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator, Generic, TypeVar

from prion._internal.dependency import Dependency, DependencyState

T = TypeVar("T")


class Syringe:
    def __init__(self) -> None:
        self._dependencies: dict[str, DependencyState[Any]] = {}

    def reset(self) -> None:
        for state in self._dependencies.values():
            state.reset()

    def __enter__(self) -> Syringe:
        return self

    def __exit__(self, *args: Any) -> None:
        self.reset()

    @contextmanager
    def override(self, name: str, provider: Any) -> Generator[None, None, None]:
        state = self._dependencies.get(name)
        if state is None:
            raise KeyError(f"unknown dependency: {name}")
        old_provider = state._provider
        old_value = state._value
        old_resolved = state._resolved
        state._provider = provider
        state._value = None
        state._resolved = False
        try:
            yield
        finally:
            state._provider = old_provider
            state._value = old_value
            state._resolved = old_resolved


class single(Dependency[T], Generic[T]):
    """Singleton dependency — provider is called once, result is cached."""

    def __init__(self) -> None:
        super().__init__("single")


class factory(Dependency[T], Generic[T]):
    """Factory dependency — provider is called on every access."""

    def __init__(self) -> None:
        super().__init__("factory")
