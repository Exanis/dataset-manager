from django import template


register = template.Library()
parent_cache = None


@register.filter(name='using_parent')
def using_parent(value, arg):
    global parent_cache
    parent_cache = arg
    return value


@register.filter(name='values_for')
def values_for(value, arg):
    return value.values_for(arg)


@register.filter(name='remaining')
def remaining(value, arg):
    return arg.max_count - len(values_for(value, arg).filter(parent=parent_cache))


@register.filter(name='is_field_valid')
def is_field_valid(value, arg):
    return value.is_field_valid(arg, parent_cache)


@register.filter(name='with_parent')
def with_parent(value, arg):
    return value.filter(parent=arg)
