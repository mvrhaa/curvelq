import numpy as np

from curvelab.curves import LinearCurve
from curvelab.pricing import discount_factor


def test_discount_factor_on_flat_curve():
    curve = LinearCurve().fit([1, 30], [5.0, 5.0])
    assert np.isclose(discount_factor(curve, 1), np.exp(-0.05))
    assert np.isclose(discount_factor(curve, 10), np.exp(-0.5))
