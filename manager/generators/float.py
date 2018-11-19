from random import random


def float_generator(t, rank):
    return str(t.min + random() * (t.max - t.min))
