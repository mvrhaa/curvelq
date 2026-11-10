import numpy as np


def discount_factor(curve, t):
    """Value today of 1 paid in t years, with continuous compounding. Curve rates are in percent."""
    rate = curve.rate(t) / 100
    return np.exp(-rate * np.array(t, dtype=float))


def price_bond(curve, coupon, years, nominal=100):
    """Price of a bond with an annual coupon (in percent) and whole years to maturity."""
    times = np.arange(1, years + 1)
    payments = np.full(years, nominal * coupon / 100)
    payments[-1] += nominal
    return np.sum(payments * discount_factor(curve, times))


class ShiftedCurve:
    """A curve with a shift in bp: short_bp up to 2Y, long_bp from 10Y, linear in between."""

    def __init__(self, curve, short_bp, long_bp):
        self.curve = curve
        self.short_bp = short_bp
        self.long_bp = long_bp

    def rate(self, t):
        shift_bp = np.interp(t, [2, 10], [self.short_bp, self.long_bp])
        return self.curve.rate(t) + shift_bp / 100


def dv01(curve, coupon, years):
    """How much the price falls when the whole curve moves up by 1 bp."""
    base = price_bond(curve, coupon, years)
    shifted = price_bond(ShiftedCurve(curve, 1, 1), coupon, years)
    return base - shifted


def scenarios(curve, coupon, years):
    """Price, DV01 and price change for a +100 bp parallel shift and a +50 bp long end steepening."""
    base = price_bond(curve, coupon, years)
    parallel = price_bond(ShiftedCurve(curve, 100, 100), coupon, years)
    steepening = price_bond(ShiftedCurve(curve, 0, 50), coupon, years)
    return {
        "price": base,
        "dv01": dv01(curve, coupon, years),
        "parallel_100bp": parallel - base,
        "steepening_50bp": steepening - base,
    }
