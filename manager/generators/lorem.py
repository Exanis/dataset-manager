from random import randint

base_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit." \
            " Nullam ultricies aliquet ligula eu finibus. Proin vitae elit a mi dignissim " \
            "molestie in sit amet arcu. Vivamus ac accumsan ligula. In vitae libero volutpat " \
            "felis pharetra aliquet sit amet at leo. Phasellus ipsum eros, efficitur non " \
            "lobortis id, tristique ac eros. Vivamus convallis mollis tortor nec pellentesque. " \
            "Sed cursus diam a odio cursus vestibulum. Donec venenatis ex ligula. " \
            "Integer non finibus neque, eu lobortis purus. Integer vitae odio rutrum dui " \
            "dignissim sodales. Praesent felis ante, consectetur sed pellentesque ac, tincidunt " \
            "ut libero. Morbi eu orci placerat, vulputate ligula id, porttitor ipsum. Mauris ligula " \
            "sem, venenatis vitae justo a, interdum aliquam enim. Donec at bibendum nulla, " \
            "non pharetra arcu. Donec et lacus lectus."


def lorem_generator(t, rank):
    length = randint(t.min, t.max)
    words = base_text.split(' ')
    result = []
    while len(result) < length:
        result.append(words[len(result) % len(words)])
    return ' '.join(result)
