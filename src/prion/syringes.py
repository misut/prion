from functools import singledispatchmethod
from types import ModuleType
from typing import Any, ParamSpec, TypeVar

from prion.collections import Tree
from prion.models import Singleton

P = ParamSpec("P")
R = TypeVar("R")


class BaseSyringe(Singleton):
    _granted: Tree[list["BaseSyringe"]] = Tree()

    @singledispatchmethod
    def grant(self, *modules: Any) -> None:  # pragma: no cover
        raise NotImplementedError()

    @grant.register
    def _(self, *module_paths: str) -> None:
        for module_path in module_paths:
            if module_path not in self._granted or self._granted[module_path] is None:
                self._granted[module_path] = []
            self._granted[module_path].append(self)

    @grant.register
    def _(self, *modules: ModuleType) -> None:
        for module in modules:
            if not module.__spec__:
                raise ValueError(f"No Module Spec Found {module}")
            self.grant(module.__spec__.name)


def list_syringes(module_path: str) -> list["BaseSyringe"] | None:
    return BaseSyringe._granted[module_path]
