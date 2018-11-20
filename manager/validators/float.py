def float_validator(val, t):
    try:
        fval = float(val)
    except ValueError:
        return False
    return t.min <= fval <= t.max
