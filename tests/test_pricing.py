import numpy as np

from curvelab.curves import LinearCurve
from curvelab.pricing import discount_factor, dv01, price_bond, scenarios


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


def test_dv01_of_zero_coupon_bond():
    curve = LinearCurve().fit([1, 30], [5.0, 5.0])
    price = price_bond(curve, 0, 10)
    assert np.isclose(dv01(curve, 0, 10), price * (1 - np.exp(-0.001)))


def test_prices_fall_when_rates_rise():
    curve = LinearCurve().fit([1, 30], [5.0, 5.0])
    result = scenarios(curve, 3.0, 10)
    assert result["dv01"] > 0
    assert result["parallel_100bp"] < result["steepening_50bp"] < 0
