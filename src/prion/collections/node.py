from collections.abc import MutableMapping
from typing import Final, Generic, Iterator, TypeVar

T = TypeVar("T")


class Node(MutableMapping[str, "Node[T]"], Generic[T]):
    _key: Final[str]
    _value: T | None
    _nodes: dict[str, "Node[T]"]

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

    def __delitem__(self, key: str) -> None:
        del self._nodes[key]

    def __getitem__(self, key: str) -> "Node[T]":
        return self._nodes[key]

    def __setitem__(self, key: str, value: "Node[T]") -> None:
        self._nodes[key] = value

    def __iter__(self) -> Iterator[str]:
        for key in self._nodes:
            yield key

    def __len__(self) -> int:
        return len(self._nodes)

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> T | None:
        return self._value

    @value.setter
    def value(self, value: T | None) -> None:
        self._value = value
