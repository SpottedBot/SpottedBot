from django.conf import settings


def enable_mod_shift(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'ENABLE_MOD_SHIFT': settings.ENABLE_MOD_SHIFT}


def enable_imgur_upload(request):

    if settings.IMGUR_CLIENT and settings.IMGUR_SECRET:
        return {'ENABLE_IMGUR_UPLOAD': True}
    return {'ENABLE_IMGUR_UPLOAD': False}
