from django.conf import settings
from django.apps import AppConfig
from .custom_appconf import NoPrefixAppConf


class SocialLoginConfig(AppConfig):
    name = 'custom_auth'


class SocialLoginSettings(NoPrefixAppConf):
    SOCIAL_SHOW_IN_ADMIN = True
    SOCIAL_FACEBOOK_KEY = ''
    SOCIAL_FACEBOOK_SECRET = ''
    SOCIAL_FACEBOOK_PERMISSIONS = []
