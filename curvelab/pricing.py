import numpy as np


def discount_factor(curve, t):
    rate = curve.rate(t) / 100
    return np.exp(-rate * np.array(t, dtype=float))


def price_bond(curve, coupon, years, nominal=100):
    times = np.arange(1, years + 1)
    payments = np.full(years, nominal * coupon / 100)
    payments[-1] += nominal
    return np.sum(payments * discount_factor(curve, times))
