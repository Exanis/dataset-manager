from random import randint


def int_generator(t, rank):
    return str(randint(t.min, t.max))
