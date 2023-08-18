import pytest

from prion.syringes import BaseSyringe


def test_syringe() -> None:
    class Syringe(BaseSyringe):
        foo = 123

    syringe_1, syringe_2 = Syringe(), Syringe()
    assert syringe_1 is syringe_2
    assert syringe_1.foo is syringe_2.foo

    with pytest.raises(ValueError):
        syringe_1.grant(123)
