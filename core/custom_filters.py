from django import template

register = template.Library()

@register.filter
def split_and_length(value, delimiter=","):
    return len(value.split(delimiter))