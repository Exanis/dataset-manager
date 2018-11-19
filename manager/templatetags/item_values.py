from django import template


register = template.Library()


@register.filter(name='values_for')
def values_for(value, arg):
    return value.values_for(arg)


@register.filter(name='remaining')
def remaining(value, arg):
    return arg.max_count - len(values_for(value, arg))


@register.filter(name='is_field_valid')
def is_field_valid(value, arg):
    return value.is_field_valid(arg)
