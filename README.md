# Prion

## Usage

```py
import random
from logging import Logger, getLogger
from prion import Syringe, single, factory

class Base(Syringe):
    single_logger: Logger = single()
    factory_logger: Logger = factory()


syringe = Base()

@syringe.single_logger
def create_single_logger() -> Logger:
    return getLogger(f"logger {random.randint(1, 100)}")

@syringe.factory_logger
def create_factory_logger() -> Logger:
    return getLogger(f"logger {random.randint(1, 100)}")
```
