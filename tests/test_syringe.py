from __future__ import annotations

import pytest

from prion import Syringe, factory, single


class Container(Syringe):
    value = single[str]()
    creator = factory[str]()


class TestSingle:
    def test_returns_same_instance(self) -> None:
        container = Container()

        @container.value
        def provide() -> str:
            return "hello"

        a = container.value
        b = container.value
        assert a is b

    def test_provider_called_once(self) -> None:
        container = Container()
        call_count = 0

        @container.value
        def provide() -> str:
            nonlocal call_count
            call_count += 1
            return "hello"

        _ = container.value
        _ = container.value
        _ = container.value
        assert call_count == 1


class TestFactory:
    def test_returns_new_instance_each_time(self) -> None:
        container = Container()

        @container.creator
        def provide() -> str:
            return str(id(object()))

        a = container.creator
        b = container.creator
        assert a is not b

    def test_provider_called_every_access(self) -> None:
        container = Container()
        call_count = 0

        @container.creator
        def provide() -> str:
            nonlocal call_count
            call_count += 1
            return "hello"

        _ = container.creator
        _ = container.creator
        _ = container.creator
        assert call_count == 3


class TestDecorator:
    def test_decorator_returns_original_function(self) -> None:
        container = Container()

        @container.value
        def provide() -> str:
            return "hello"

        assert callable(provide)
        assert provide() == "hello"

    def test_unregistered_dependency_is_callable(self) -> None:
        container = Container()
        slot = container.value
        assert callable(slot)


class TestIsolation:
    def test_separate_instances_are_independent(self) -> None:
        a = Container()
        b = Container()

        @a.value
        def provide_a() -> str:
            return "a"

        @b.value
        def provide_b() -> str:
            return "b"

        assert a.value == "a"
        assert b.value == "b"

    def test_unregistered_dependency_returns_slot(self) -> None:
        container = Container()

        @container.value
        def provide() -> str:
            return "ok"

        # factory has no provider registered — returns the slot, not a value
        slot = container.creator
        assert callable(slot)
