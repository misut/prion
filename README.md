# Prion

A dependency injection framework using pure Python. No external dependencies.

## Installation

```sh
pip install prion
```

## Usage

Define a container by subclassing `Syringe` and declaring dependencies with `single[T]()` or `factory[T]()`.

```pycon
>>> from prion import Syringe, single, factory

>>> class AppSyringe(Syringe):
...     config = single[dict]()
...     session = factory[dict]()

```

Create an instance and register providers using decorators.

```pycon
>>> syringe = AppSyringe()

>>> @syringe.config
... def create_config() -> dict:
...     return {"debug": True}

>>> @syringe.session
... def create_session() -> dict:
...     return {}

```

Access dependencies as attributes.

```pycon
>>> syringe.config is syringe.config
True

>>> syringe.session is not syringe.session
True

```

## Dependency Wiring

Providers can receive other dependencies as parameters. Parameter names are matched to dependency names automatically.

```pycon
>>> class WiredSyringe(Syringe):
...     config = single[dict]()
...     greeting = single[str]()

>>> syringe = WiredSyringe()

>>> @syringe.config
... def create_config() -> dict:
...     return {"name": "world"}

>>> @syringe.greeting
... def create_greeting(config: dict) -> str:
...     return f"hello {config['name']}"

>>> syringe.greeting
'hello world'

```

Circular dependencies are detected at resolve time with a `RuntimeError`.

## Lifecycle

Use `reset()` to clear all cached singletons, or use the container as a context manager.

```pycon
>>> syringe = AppSyringe()

>>> @syringe.config
... def create_config() -> dict:
...     return {"debug": True}

>>> with syringe:
...     _ = syringe.config
...
>>> # singleton cache is cleared after exiting the context

```

## Testing

Use `override()` to temporarily replace a provider in tests.

```pycon
>>> syringe = AppSyringe()

>>> @syringe.config
... def create_config() -> dict:
...     return {"debug": True}

>>> syringe.config
{'debug': True}

>>> with syringe.override("config", lambda: {"debug": False}):
...     syringe.config
{'debug': False}

>>> syringe.config
{'debug': True}

```

## Strategies

| Strategy      | Behavior                         |
| ------------- | -------------------------------- |
| `single[T]()` | Creates once, returns cached    |
| `factory[T]()` | Creates a new instance each time |

## License

MIT
