def float_validator(val, t):
    fval = float(val)
    return t.min <= fval <= t.max
