import numpy as np

from curvelab.curves import LinearCurve
from curvelab.pricing import discount_factor, price_bond


def test_discount_factor_on_flat_curve():
    curve = LinearCurve().fit([1, 30], [5.0, 5.0])
    assert np.isclose(discount_factor(curve, 1), np.exp(-0.05))
    assert np.isclose(discount_factor(curve, 10), np.exp(-0.5))


def test_bond_near_par_when_curve_is_flat_at_coupon():
    curve = LinearCurve().fit([1, 30], [5.0, 5.0])
    price = price_bond(curve, 5.0, 10)
    assert abs(price - 100) < 1.5


def test_bond_exactly_at_par_with_compounding_adjustment():
    curve = LinearCurve().fit([1, 30], [5.0, 5.0])
    coupon = (np.exp(0.05) - 1) * 100
    price = price_bond(curve, coupon, 10)
    assert np.isclose(price, 100)
