import numpy as np
from scipy.interpolate import CubicSpline
from curvelab.curves import LinearCurve, SplineCurve, ns_rate

class Curve:
    def fit(self,maturities,yields):
        raise NotImplementedError
    def rate(self,t):
        raise NotImplementedError

class LinearCurve(Curve):
    def fit(self, maturities, yields):
        self.maturities = np.array(maturities, dtype=float)
        self.yields = np.array(yields, dtype=float)
        return self

    def rate(self, t):
        return np.interp(t, self.maturities, self.yields)

class SplineCurve(Curve):
    def fit(self,maturities,yields):
        self.spline = CubicSpline(maturities,yields,bc_type="natural")
        return self
    def rate(self,t):
        return self.spline(t)

    def ns_rate(t, b0, b1, b2, lam):
        """Nelson-Siegel rate for maturity t (in years).
        b0 is the level: the rate at very long maturities.
        b1 is the slope: the short end is b0 + b1, the effect fades with maturity.
        b2 is the curvature: a hump in the middle, zero at both ends.
        lam sets where the hump is: bigger lam moves it to shorter maturities.
        """
        t = np.array(t, dtype=float)
        x = lam * t
        slope = (1 - np.exp(-x)) / x
        hump = slope - np.exp(-x)
        return b0 + b1 * slope + b2 * hump

    def test_ns_long_end_goes_to_b0():
        rate = ns_rate(10000, 3.0, -2.0, 1.0, 0.5)
        assert abs(rate - 3.0) < 0.001


    def test_ns_short_end_goes_to_b0_plus_b1():
        rate = ns_rate(0.000001, 3.0, -2.0, 1.0, 0.5)
        assert abs(rate - 1.0) < 0.001