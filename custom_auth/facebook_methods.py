import facebook
from django.conf import settings
from django.shortcuts import reverse
from urllib.parse import urlencode
from django.contrib.auth import login
from django.contrib import messages


app_id = settings.FACEBOOK_KEY
app_secret = settings.FACEBOOK_SECRET


def get_graph():
    graph = facebook.GraphAPI(version='2.7')
    graph.access_token = graph.get_app_access_token(app_id, app_secret)
    return graph


graph = get_graph()


def canv_url(request):
    # Generates the canvas_url used by facebook to redirect after auth

    if request.is_secure():
        return 'https://' + request.get_host() + reverse('custom_auth:facebook_login_response')
    else:
        return 'http://' + request.get_host() + reverse('custom_auth:facebook_login_response')


def auth_url(request):
    # Returns the facebook auth url using the current app's domain

    canvas_url = canv_url(request)
    perms = settings.FACEBOOK_PERMISSIONS
    url = "https://www.facebook.com/dialog/oauth?"
    kvps = {'client_id': app_id, 'redirect_uri': canvas_url}
    if perms:
        kvps['scope'] = ",".join(perms)

    return url + urlencode(kvps)


def debug_token(token):
    # Returns the debug string for token

    return graph.debug_access_token(token, app_id, app_secret)


def login_successful(code, request):

    canvas_url = canv_url(request)
    token_info = graph.get_access_token_from_code(code, canvas_url, app_id, app_secret)
    access_token = token_info['access_token']
    try:
        token_expires = token_info['expires']
    except:
        token_expires = 999999999999

    debug = debug_token(access_token)['data']

    social_id = debug['user_id']

    extra_data = graph.get_object(str(social_id) + '/?fields=name,first_name,link')
    name = extra_data['name']
    first_name = extra_data['first_name']
    link = extra_data['link']
    from .models import FacebookUser
    new = FacebookUser.create_or_update(social_id, access_token, token_expires, first_name, name, link)

    if new.user.is_active:
        login(request, new.user)
        messages.add_message(request, messages.SUCCESS, 'Olá, ' + first_name + '!')
    else:
        messages.add_message(request, messages.ERROR, 'Essa conta foi desativada!')

    return request


def login_canceled(request):
    messages.add_message(request, messages.ERROR, 'Oops! Algo de errado aconteceu!')

    return request
