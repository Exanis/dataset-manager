def int_validator(val, t):
    fval = int(val)
    return t.min <= fval <= t.max
