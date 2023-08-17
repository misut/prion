from typing import Any, ClassVar


class _SingletonBase(type):
    _instances: ClassVar[dict[type, "Singleton"]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> "Singleton":
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=_SingletonBase):
    ...
