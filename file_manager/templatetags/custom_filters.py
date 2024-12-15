from django import template

register = template.Library()

@register.filter
def split_string(value, arg):
    return value.split(arg)[-1]  # Split by the given argument and return the last part.
