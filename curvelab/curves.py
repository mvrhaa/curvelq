import numpy as np
from scipy.interpolate import CubicSpline


class Curve:
    def fit(self, maturities, yields):
        raise NotImplementedError

    def rate(self, t):
        raise NotImplementedError


class LinearCurve(Curve):
    def fit(self, maturities, yields):
        self.maturities = np.array(maturities, dtype=float)
        self.yields = np.array(yields, dtype=float)
        return self

    def rate(self, t):
        return np.interp(t, self.maturities, self.yields)


class SplineCurve(Curve):
    def fit(self, maturities, yields):
        self.spline = CubicSpline(maturities, yields, bc_type="natural")
        return self

    def rate(self, t):
        return self.spline(t)


def ns_factors(t, lam):
    t = np.array(t, dtype=float)
    x = lam * t
    slope = (1 - np.exp(-x)) / x
    hump = slope - np.exp(-x)
    return slope, hump


def ns_rate(t, b0, b1, b2, lam):
    """
    Nelson-Siegel rate for maturity t (in years).

    b0 is the level: the rate at very long maturities.
    b1 is the slope: the short end is b0 + b1, the effect fades with maturity.
    b2 is the curvature: a hump in the middle, zero at both ends.
    lam sets where the hump is: bigger lam moves it to shorter maturities.
    """
    slope, hump = ns_factors(t, lam)
    return b0 + b1 * slope + b2 * hump


def fit_ns_betas(maturities, yields, lam):
    slope, hump = ns_factors(maturities, lam)
    X = np.column_stack([np.ones(len(slope)), slope, hump])
    y = np.array(yields, dtype=float)
    betas = np.linalg.lstsq(X, y, rcond=None)[0]
    return betas


LAMBDAS = np.arange(0.1, 3.01, 0.05)


class NelsonSiegelCurve(Curve):
    def fit(self, maturities, yields):
        y = np.array(yields, dtype=float)
        best_error = None
        for lam in LAMBDAS:
            betas = fit_ns_betas(maturities, y, lam)
            fitted = ns_rate(maturities, betas[0], betas[1], betas[2], lam)
            error = np.sum((fitted - y) ** 2)
            if best_error is None or error < best_error:
                best_error = error
                self.betas = betas
                self.lam = lam
        return self

    def rate(self, t):
        return ns_rate(t, self.betas[0], self.betas[1], self.betas[2], self.lam)
