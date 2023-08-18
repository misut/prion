import pytest

from prion.collections import Node, Tree


def test_node() -> None:
    node = Node[int]("foo", 123)
    assert node.value == 123

    node.value = 456
    assert node.value == 456

    with pytest.raises(TypeError):
        123 in node

    node["bar"] = Node[int]("bar", 456)
    assert "bar" in node

    with pytest.raises(KeyError):
        node["baz"]

    node["baz"] = Node[int]("baz", 789)
    assert len(node) == 2

    assert set(node.keys()) == {"bar", "baz"}
    assert set(n.value for n in node.values()) == {456, 789}

    del node["baz"]
    assert len(node) == 1

def test_tree() -> None:
    tree = Tree[int]()
    tree["foo"] = 123
    assert tree["foo"] == 123
    with pytest.raises(TypeError):
        123 in tree
    with pytest.raises(KeyError):
        tree["bar"]
    with pytest.raises(KeyError):
        del tree["bar"]

    tree["foo.bar.baz"] = 456
    assert tree["foo.bar.baz"] == 456
    assert len(tree) == 2
    assert list(tree) == ["foo.bar.baz", "foo"]
    with pytest.raises(IndexError):
        tree["foo.bar"]
    with pytest.raises(KeyError):
        del tree["bar"]

    del tree["foo"]
    with pytest.raises(KeyError):
        del tree["foo"]
    assert len(tree) == 1
    assert list(tree) == ["foo.bar.baz"]
