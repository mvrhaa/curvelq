import numpy as np
from curvelab.curves import LinearCurve, SplineCurve


MATURITIES = [0.25,1,2,5,10,30]
YIELDS=[3.5,3.2,2.8,2.5,2.7,3.0]

def test_linear_passes_through_points():
    curve = LinearCurve().fit(MATURITIES,YIELDS)
    assert np.allclose(curve.rate(MATURITIES),YIELDS)
    assert np.allclose(curve.rate(MATURITIES),YIELDS)

def test_linear_is_flat_outside_range():
    curve=LinearCurve().fit(MATURITIES,YIELDS)
    assert curve.rate(0.01) == 3.5
    assert curve.rate(50) == 3.0

def test_spline_passes_through_points():
    curve = SplineCurve().fit(MATURITIES,YIELDS)
    assert np.allclose(curve.rate(MATURITIES),YIELDS)