from django.conf import settings
from django import template
import random


register = template.Library()


ads_active = settings.ADS_ACTIVE
dev_ad = settings.DEV_AD
spotted_ad = settings.SPOTTED_AD


@register.simple_tag
def ad_active():
    print(ads_active)
    if ads_active:
        return True
    return False


@register.simple_tag
def ad_load():
    if not spotted_ad:
        return False
    return True


@register.simple_tag
def dev_ad_init():
    return dev_ad


@register.simple_tag
def spotted_ad_init():
    return spotted_ad


@register.simple_tag
def ad_value():
    if random.random() > 0.3:
        return dev_ad
    else:
        return spotted_ad
