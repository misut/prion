# Prion

A dependency injection framework using pure Python. No external dependencies.

## Installation

```sh
pip install prion
```

## Usage

Define a container by subclassing `Syringe` and declaring dependencies with `single()` or `factory()`.

```py
from logging import Logger, getLogger
from prion import Syringe, single, factory

class AppSyringe(Syringe):
    logger: Logger = single()
    handler: Logger = factory()
```

Create an instance and register providers using decorators.

```py
syringe = AppSyringe()

@syringe.logger
def create_logger() -> Logger:
    return getLogger("app")

@syringe.handler
def create_handler() -> Logger:
    return getLogger("handler")
```

Access dependencies as attributes.

```py
# single() returns the same instance every time
assert syringe.logger is syringe.logger

# factory() returns a new instance every time
assert syringe.handler is not syringe.handler
```

## Strategies

| Strategy    | Behavior                          |
| ----------- | --------------------------------- |
| `single()`  | Creates once, returns cached      |
| `factory()` | Creates a new instance each time  |

## License

MIT
