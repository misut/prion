from collections.abc import Container
from typing import Final, Generic, TypeVar

T = TypeVar("T", covariant=True)
U = TypeVar("U")

ROOT_PATH: Final = "$"


class _Node(Container[str], Generic[T]):
    _key: Final[str]
    _value: T | None
    _nodes: dict[str, "_Node[T]"]

    def __init__(self, key: str, value: T | None = None) -> None:
        self._key = key
        self._value = value
        self._nodes = {}

    def __contains__(self, key: object) -> bool:
        match key:
            case str(key):
                return key in self._nodes
            case _:
                raise TypeError()

    def __getitem__(self, key: str) -> "_Node[T]":
        return self._nodes[key]

    def __setitem__(self, key: str, value: T | None) -> None:
        self._nodes[key] = _Node[T](key, value)

    @property
    def value(self) -> T | None:
        return self._value

    @value.setter
    def value(self, value: T | None) -> None:
        self._value = value


class Tree(Container[str], Generic[T]):
    _root: _Node[T]

    def __init__(self) -> None:
        self._root = _Node(ROOT_PATH)

    def __contains__(self, path: object) -> bool:
        match path:
            case str(path):
                keys = path.split(".")
            case _:
                raise TypeError()

        node = self._root
        for key in keys:
            if key not in node:
                return False

            node = node[key]

        return True

    def __getitem__(self, path: str) -> T:
        keys = path.split(".")

        node = self._root
        for key in keys:
            node = node[key]

        if node.value is None:
            raise IndexError()
        return node.value

    def __setitem__(self, path: str, value: T | None) -> None:
        keys = path.split(".")

        node = self._root
        for key in keys:
            if key not in node:
                node[key] = None

            node = node[key]

        node.value = value
