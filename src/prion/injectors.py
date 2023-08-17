import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, Generic, ParamSpec, TypeVar

from prion.syringes import list_syringes

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T", covariant=True)


def _inject_function(callable: Callable[P, R]) -> Callable[P, R]:
    @wraps(callable)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        module = inspect.getmodule(callable)
        if not (module and module.__spec__):
            return callable(*args, **kwargs)

        syringes = list_syringes(module.__spec__.name)
        if not syringes:
            return callable(*args, **kwargs)

        signature = inspect.signature(callable)
        for param in signature.parameters.values():
            if not isinstance(param.default, _Injector):
                continue

            for syringe in syringes:
                if hasattr(syringe, param.default._attr):
                    kwargs[param.name] = getattr(syringe, param.default._attr)
                    break

        return callable(*args, **kwargs)

    return wrapper


def inject(callable: Callable[P, R]) -> Callable[P, R]:
    if inspect.isfunction(callable):
        return _inject_function(callable)

    raise ValueError(f"Not Supported Callable Type {type(callable)}")


class _Injector(Generic[T]):
    _attr: str

    def __init__(self, attr: str) -> None:
        self._attr = attr


def injector(attr: str) -> Any:
    return _Injector(attr)
