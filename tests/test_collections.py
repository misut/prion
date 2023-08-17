import pytest

from prion.collections import Tree


def test_tree() -> None:
    tree = Tree[int]()
    tree["foo"] = 123
    assert tree["foo"] == 123

    with pytest.raises(KeyError):
        tree["bar"]

    tree["foo.bar.baz"] = 456
    assert tree["foo.bar.baz"] == 456

    with pytest.raises(IndexError):
        tree["foo.bar"]

    with pytest.raises(KeyError):
        tree["foo.bar.foo"]
