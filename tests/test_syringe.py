from __future__ import annotations

import threading

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


class TestThreadSafety:
    def test_single_is_thread_safe(self) -> None:
        container = Container()
        call_count = 0
        lock = threading.Lock()

        @container.value
        def provide() -> str:
            nonlocal call_count
            with lock:
                call_count += 1
            return "hello"

        results: list[str] = []

        def access() -> None:
            results.append(container.value)

        threads = [threading.Thread(target=access) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert call_count == 1
        assert all(r == "hello" for r in results)


class TestLifecycle:
    def test_reset_clears_singleton_cache(self) -> None:
        container = Container()
        call_count = 0

        @container.value
        def provide() -> str:
            nonlocal call_count
            call_count += 1
            return f"v{call_count}"

        assert container.value == "v1"
        assert container.value == "v1"
        assert call_count == 1

        container.reset()

        assert container.value == "v2"
        assert call_count == 2

    def test_context_manager_resets_on_exit(self) -> None:
        container = Container()
        call_count = 0

        @container.value
        def provide() -> str:
            nonlocal call_count
            call_count += 1
            return f"v{call_count}"

        with container:
            assert container.value == "v1"

        # after exit, singleton cache is cleared
        assert container.value == "v2"
        assert call_count == 2


class WiredContainer(Syringe):
    config = single[dict]()
    greeting = single[str]()
    message = factory[str]()


class TestDependencyWiring:
    def test_provider_receives_other_dependency(self) -> None:
        container = WiredContainer()

        @container.config
        def create_config() -> dict:
            return {"name": "world"}

        @container.greeting
        def create_greeting(config: dict) -> str:
            return f"hello {config['name']}"

        assert container.greeting == "hello world"

    def test_factory_receives_singleton(self) -> None:
        container = WiredContainer()
        call_count = 0

        @container.config
        def create_config() -> dict:
            nonlocal call_count
            call_count += 1
            return {"v": call_count}

        @container.message
        def create_message(config: dict) -> str:
            return f"v{config['v']}"

        assert container.message == "v1"
        assert container.message == "v1"
        assert call_count == 1  # config is singleton, called once

    def test_circular_dependency_raises(self) -> None:
        class Circular(Syringe):
            a = single[str]()
            b = single[str]()

        container = Circular()

        @container.a
        def create_a(b: str) -> str:
            return f"a({b})"

        @container.b
        def create_b(a: str) -> str:
            return f"b({a})"

        with pytest.raises(RuntimeError, match="circular dependency"):
            _ = container.a

    def test_unknown_params_are_ignored(self) -> None:
        container = WiredContainer()

        @container.config
        def create_config(unknown_param: str = "default") -> dict:
            return {"key": unknown_param}

        assert container.config == {"key": "default"}


class TestOverride:
    def test_override_replaces_provider(self) -> None:
        container = Container()

        @container.value
        def provide() -> str:
            return "original"

        assert container.value == "original"

        with container.override("value", lambda: "mocked"):
            assert container.value == "mocked"

        assert container.value == "original"

    def test_override_restores_cached_singleton(self) -> None:
        container = Container()
        call_count = 0

        @container.value
        def provide() -> str:
            nonlocal call_count
            call_count += 1
            return f"v{call_count}"

        assert container.value == "v1"

        with container.override("value", lambda: "mock"):
            assert container.value == "mock"

        # original cached value is restored, not re-created
        assert container.value == "v1"
        assert call_count == 1

    def test_override_unknown_dependency_raises(self) -> None:
        container = Container()

        with pytest.raises(KeyError, match="unknown dependency"):
            with container.override("nonexistent", lambda: "x"):
                pass
