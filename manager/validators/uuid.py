from uuid import UUID


def uuid_validator(val, t):
    try:
        UUID(val)
        return True
    except ValueError:
        return False
