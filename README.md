# Prion

`Prion` is a dependency injection framework implemented with pure Python.

## Installation and usage

### Installation

The package is available on the [PyPi](https://test.pypi.org/project/prion/):

```sh
pip install prion
```

### Usage

```py
from prion import BaseSyringe, inject, injector

# First, create a class extending `BaseSyringe`.
class Syringe(BaseSyringe):
    # This class has dependencies as its attributes.
    foo = 123
    bar = 456

# Second, add `@inject` and `injector()` where you want to inject dependencies.
@inject
def baz(foo = injector("foo"), bar = injector("bar")):
    println(foo, bar)

# Finally, grant a package to be injected.
syringe = Syringe()
syringe.grant(__name__)

# You can call `bar()` without given parameters.
bar()
```
