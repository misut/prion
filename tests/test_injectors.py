import pytest

from prion.injectors import inject


def test_inject() -> None:
    @inject
    def foo() -> None:
        pass

    @inject
    async def bar() -> None:
        pass

    with pytest.raises(ValueError):

        @inject
        class Baz:
            ...
