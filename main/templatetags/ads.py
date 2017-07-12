from django import template

register = template.Library()


@register.filter(name='next')
def dj_next(gen):
    try:
        return next(gen)
    except StopIteration:
        return False
