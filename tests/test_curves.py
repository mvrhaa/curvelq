import numpy as np

from curvelab.curves import LinearCurve, NelsonSiegelCurve, SplineCurve, ns_rate

MATURITIES = [0.25, 1, 2, 5, 10, 30]
YIELDS = [3.5, 3.2, 2.8, 2.5, 2.7, 3.0]


def test_linear_passes_through_points():
    curve = LinearCurve().fit(MATURITIES, YIELDS)
    assert np.allclose(curve.rate(MATURITIES), YIELDS)


def test_linear_is_flat_outside_range():
    curve = LinearCurve().fit(MATURITIES, YIELDS)
    assert curve.rate(0.01) == 3.5
    assert curve.rate(50) == 3.0


def test_spline_passes_through_points():
    curve = SplineCurve().fit(MATURITIES, YIELDS)
    assert np.allclose(curve.rate(MATURITIES), YIELDS)


def test_ns_long_end_goes_to_b0():
    rate = ns_rate(10000, 3.0, -2.0, 1.0, 0.5)
    assert abs(rate - 3.0) < 0.001


def test_ns_short_end_goes_to_b0_plus_b1():
    rate = ns_rate(0.000001, 3.0, -2.0, 1.0, 0.5)
    assert abs(rate - 1.0) < 0.001


def test_ns_recovers_known_parameters():
    maturities = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 15, 20, 30]
    yields = ns_rate(maturities, 3.0, -2.0, 1.0, 0.5)
    curve = NelsonSiegelCurve().fit(maturities, yields)
    assert np.allclose(curve.betas, [3.0, -2.0, 1.0])
    assert abs(curve.lam - 0.5) < 0.001
