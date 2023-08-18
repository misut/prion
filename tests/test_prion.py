import pytest

from prion.injectors import inject, injector
from prion.syringes import BaseSyringe


def test_prion() -> None:
    @inject
    def fun_foo(foo: int = injector("foo")) -> int:
        return foo

    class SyringeFoo(BaseSyringe):
        foo = 123

    syringe_foo = SyringeFoo()
    syringe_foo.grant(__name__)
    assert fun_foo() == 123

    @inject
    def fun_bar(bar: int = injector("bar")) -> int:
        return bar

    class SyringeBar(BaseSyringe):
        bar = 456

    syringe_bar = SyringeBar()
    from tests import test_prion

    tmp = test_prion.__name__
    test_prion.__name__ = ""
    with pytest.raises(ValueError):
        syringe_bar.grant(test_prion)

    test_prion.__name__ = tmp
    syringe_bar.grant(test_prion)
    assert fun_bar() == 456
