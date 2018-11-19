import string
from random import choice, randint


def str_generator(t, rank):
    accepted = string.ascii_letters + string.digits
    return ''.join([choice(accepted) for _ in range(randint(t.min, t.max))])
