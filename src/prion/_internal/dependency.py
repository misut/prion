from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from prion.syringe import Syringe


class DependencyState:
    __slots__ = ("_strategy", "_provider", "_value", "_resolved")

    def __init__(self, strategy: str) -> None:
        self._strategy = strategy
        self._provider: Callable[..., Any] | None = None
        self._value: Any = None
        self._resolved = False

    def __call__(self, provider: Callable[..., Any]) -> Callable[..., Any]:
        self._provider = provider
        return provider

    def resolve(self) -> Any:
        if self._provider is None:
            raise RuntimeError("no provider registered for this dependency")
        if self._strategy == "single":
            if not self._resolved:
                self._value = self._provider()
                self._resolved = True
            return self._value
        return self._provider()


class Dependency:
    __slots__ = ("_strategy", "_attr")

    def __init__(self, strategy: str) -> None:
        self._strategy = strategy
        self._attr: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr = name

    def __get__(self, obj: Syringe | None, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        state = obj._dependencies.get(self._attr)
        if state is None:
            state = DependencyState(self._strategy)
            obj._dependencies[self._attr] = state
        if state._provider is None:
            return state
        return state.resolve()
