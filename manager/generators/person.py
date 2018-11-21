from random import randint
from faker import Faker
from django.conf import settings


def person_generator(t, rank):
    fake = Faker(settings.LANGUAGE_CODE)
    profile = fake.simple_profile()
    data = randint(0, 3)
    if data == 0:
        return profile['name']
    elif data == 1:
        return profile['mail']
    elif data == 2:
        return fake.phone_number()
    else:
        return profile['address']
