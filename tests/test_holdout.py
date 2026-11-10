from curvelab import config
from curvelab.holdout import split_maturities


def test_split_hides_three_maturities():
    known, hidden = split_maturities(config.MATURITIES)
    assert hidden == [2, 7, 15]
    assert known == [0.25, 0.5, 1, 3, 5, 10, 20, 30]
