from faker import Faker


fake = Faker()


def _fake_date(t, format):
    min = str(t.min) if t.min < 0 else "+" + str(t.min)
    max = str(t.max) if t.max < 0 else "+" + str(t.max)
    return fake.date_between(start_date=min + 'd', end_date=max + 'd').strftime(format)


def date_generator(t, rank):
    return _fake_date(t, '%Y-%m-%d')


def datetime_generator(t, rank):
    return "{}T{}".format(
        _fake_date(t, '%Y-%m-%d'),
        fake.time()
    )


def time_generator(t, rank):
    return fake.time()
