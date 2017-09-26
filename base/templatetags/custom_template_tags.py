from os import path
from django import template

register = template.Library()


@register.simple_tag
def filetype(filename):
    return path.splitext(filename)[-1]
