import numpy as np


def discount_factor(curve, t):
    rate = curve.rate(t) / 100
    return np.exp(-rate * np.array(t, dtype=float))


def price_bond(curve, coupon, years, nominal=100):
    times = np.arange(1, years + 1)
    payments = np.full(years, nominal * coupon / 100)
    payments[-1] += nominal
    return np.sum(payments * discount_factor(curve, times))


class ShiftedCurve:
    def __init__(self, curve, short_bp, long_bp):
        self.curve = curve
        self.short_bp = short_bp
        self.long_bp = long_bp

    def rate(self, t):
        shift_bp = np.interp(t, [2, 10], [self.short_bp, self.long_bp])
        return self.curve.rate(t) + shift_bp / 100


def dv01(curve, coupon, years):
    base = price_bond(curve, coupon, years)
    shifted = price_bond(ShiftedCurve(curve, 1, 1), coupon, years)
    return base - shifted


def scenarios(curve, coupon, years):
    base = price_bond(curve, coupon, years)
    parallel = price_bond(ShiftedCurve(curve, 100, 100), coupon, years)
    steepening = price_bond(ShiftedCurve(curve, 0, 50), coupon, years)
    return {
        "price": base,
        "dv01": dv01(curve, coupon, years),
        "parallel_100bp": parallel - base,
        "steepening_50bp": steepening - base,
    }
