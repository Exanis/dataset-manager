def options_validator(val, t):
    return val in [o.name for o in t.options]
