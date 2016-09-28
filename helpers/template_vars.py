# useful to quick load template variables

from social.apps.django_app.default.models import UserSocialAuth

from app.models import Spotted


def load_index(user):
    return_vars = {}

    if user.is_authenticated():
        uid = user.profile.global_id
        spots = Spotted.objects.filter(target=uid).filter(spam=False).filter(dismissed=False)
        return_vars['spots'] = spots

    # Add more variables to load and add them to return_vars

    return return_vars


def load_mod():
    return_vars = {}
    spots = Spotted.objects.filter(spam=True)
    return_vars['spots'] = spots

    # Add more variables to load and append to return_vars

    return return_vars


def load_profile(user):
    return_vars = {}
    spots = Spotted.objects.filter(author=user).filter(spam=False)
    return_vars['spots'] = spots

    # Add more variables to load and append to return_vars

    return return_vars
