import numpy as np

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