HIDDEN = [2, 7, 15]


def split_maturities(maturities, hidden=HIDDEN):
    known = [m for m in maturities if m not in hidden]
    hidden = [m for m in maturities if m in hidden]
    return known, hidden
