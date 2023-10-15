from django import template
from django.utils.html import mark_safe

register = template.Library()

@register.filter
@mark_safe
def target_blank(value):
    return value.replace('<a ', '<a target="_blank" ')