# Prion

A dependency injection framework using pure Python. No external dependencies.

## Installation

```sh
pip install prion
```

## Usage

Define a container by subclassing `Syringe` and declaring dependencies with `single()` or `factory()`.

```pycon
>>> from prion import Syringe, single, factory

>>> class AppSyringe(Syringe):
...     config: dict = single()
...     session: dict = factory()

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

## Strategies

| Strategy    | Behavior                          |
| ----------- | --------------------------------- |
| `single()`  | Creates once, returns cached      |
| `factory()` | Creates a new instance each time  |

## License

MIT
