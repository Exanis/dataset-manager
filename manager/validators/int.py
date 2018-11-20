def int_validator(val, t):
    try:
        fval = int(val)
    except ValueError:
        return False
    return t.min <= fval <= t.max
