from django import template
import math

register = template.Library()


@register.filter(name='stat_order')
def stat_order(value):
    units = {
        1: 'K',
        2: 'M',
        3: 'G'
    }
    magnitude = int(math.log10(value))
    if magnitude < 3:
        return str(value)
    base_100_order = magnitude // 3
    return "{}{}".format(
        "{:.1f}".format(value / (1000 ** base_100_order)).rstrip('0').rstrip('.'),
        units[base_100_order]
    )
