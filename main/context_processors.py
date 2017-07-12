from django.conf import settings
import random


def enable_mod_shift(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'ENABLE_MOD_SHIFT': settings.ENABLE_MOD_SHIFT}


def enable_imgur_upload(request):

    if settings.IMGUR_CLIENT and settings.IMGUR_SECRET:
        return {'ENABLE_IMGUR_UPLOAD': True}
    return {'ENABLE_IMGUR_UPLOAD': False}


def enable_ad_tag(request):

    ads_active = settings.ADS_ACTIVE
    dev_ad = settings.DEV_AD
    spotted_ad = settings.SPOTTED_AD or dev_ad
    ads_approved = settings.ADS_APPROVED
    ad_test = settings.AD_TEST

    resp = {'ADS_APPROVED': ads_approved, 'AD_ACTIVE': ads_active, 'AD_TEST': ad_test}

    if ads_active:
        if random.random() > 0.3:
            resp['AD_CLIENT'] = dev_ad
            return resp
        else:
            resp['AD_CLIENT'] = spotted_ad
            return resp
    return resp


def ad_slot(request):
    def slotter():
        for slot in settings.AD_SLOTS:
            yield slot
    return {"AD_SLOT": slotter()}
