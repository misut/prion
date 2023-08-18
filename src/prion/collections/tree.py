from collections.abc import MutableMapping
from typing import Final, Generic, Iterator, TypeVar

from prion.collections.node import Node

T = TypeVar("T")

ROOT_KEY: Final = "$"


class Tree(MutableMapping[str, T], Generic[T]):
    _root: Node[T]

    def __init__(self, node: Node[T] | None = None) -> None:
        self._root = Node(ROOT_KEY) if node is None else node

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

        return node.value is not None

    def __delitem__(self, path: str) -> None:
        keys = path.split(".")

        node = self._root
        for key in keys:
            if key not in node:
                raise KeyError()
            node = node[key]

        if node.value is None:
            raise KeyError()
        node.value = None

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
                node[key] = Node(key)

            node = node[key]

        node.value = value

    def __iter__(self) -> Iterator[str]:
        root = self._root
        prefix = "" if root.key == ROOT_KEY else root.key
        for child in root.values():
            for path in Tree(child):
                yield f"{prefix}.{path}" if prefix else path

        if root.key != ROOT_KEY and root.value is not None:
            yield root.key

    def __len__(self) -> int:
        res = 0 if self._root.value is None else 1
        for node in self._root.values():
            res += len(Tree(node))
        return res
