from django import template

register = template.Library()


@register.filter
def split(text, separator):
    """Split a string by separator."""
    return text.split(separator)
