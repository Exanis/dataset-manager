def lorem_validator(val, t):
    words = len(val.split(' '))
    return t.min <= words <= t.max
