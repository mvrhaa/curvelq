import numpy as np


def discount_factor(curve, t):
    rate = curve.rate(t) / 100
    return np.exp(-rate * np.array(t, dtype=float))
