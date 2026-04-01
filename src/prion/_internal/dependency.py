from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar, overload

if TYPE_CHECKING:
    from typing_extensions import Self

    from prion.syringe import Syringe

T = TypeVar("T")


class DependencyState(Generic[T]):
    __slots__ = ("_strategy", "_provider", "_value", "_resolved", "_lock")

    def __init__(self, strategy: str) -> None:
        self._strategy = strategy
        self._provider: Callable[..., T] | None = None
        self._value: T | None = None
        self._resolved = False
        self._lock = threading.Lock()

    def __call__(self, provider: Callable[..., T]) -> Callable[..., T]:
        self._provider = provider
        return provider

    def resolve(self) -> T:
        if self._provider is None:
            raise RuntimeError("no provider registered for this dependency")
        if self._strategy == "single":
            if not self._resolved:
                with self._lock:
                    if not self._resolved:
                        self._value = self._provider()
                        self._resolved = True
            assert self._value is not None
            return self._value
        return self._provider()

    def reset(self) -> None:
        with self._lock:
            self._value = None
            self._resolved = False


class Dependency(Generic[T]):
    __slots__ = ("_strategy", "_attr")

    def __init__(self, strategy: str) -> None:
        self._strategy = strategy
        self._attr: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr = name

    @overload
    def __get__(self, obj: None, objtype: type | None = None) -> Self: ...

    @overload
    def __get__(
        self, obj: Syringe, objtype: type | None = None
    ) -> DependencyState[T]: ...

    def __get__(self, obj: Syringe | None, objtype: type | None = None) -> Any:
        if obj is None:
            return self  # type: ignore[return-value]
        state = obj._dependencies.get(self._attr)
        if state is None:
            state = DependencyState[T](self._strategy)
            obj._dependencies[self._attr] = state
        if state._provider is None:
            return state
        return state.resolve()
