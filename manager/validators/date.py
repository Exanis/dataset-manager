from datetime import datetime


def date_validator(val, t):
    try:
        datetime.strptime(val, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def datetime_validator(val, t):
    try:
        datetime.strptime(val, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        return False


def time_validator(val, t):
    try:
        datetime.strptime(val, "%H:%M:%S")
        return True
    except ValueError:
        return False
