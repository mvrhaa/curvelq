import pandas as pd

from curvelab import config
from curvelab.curves import NelsonSiegelCurve, ns_rate
from curvelab.holdout import holdout_error, split_maturities


def test_split_hides_three_maturities():
    known, hidden = split_maturities(config.MATURITIES)
    assert hidden == [2, 7, 15]
    assert known == [0.25, 0.5, 1, 3, 5, 10, 20, 30]


def test_holdout_error_is_zero_for_exact_ns_curve():
    yields = ns_rate(config.MATURITIES, 3.0, -2.0, 1.0, 0.5)
    row = pd.Series(yields, index=config.MATURITIES)
    errors = holdout_error(NelsonSiegelCurve(), row)
    assert errors.abs().max() < 0.001
