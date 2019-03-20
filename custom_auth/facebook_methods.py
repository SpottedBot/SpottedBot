import facebook
from django.conf import settings
from django.shortcuts import reverse
from urllib.parse import urlencode, quote, unquote
from django.contrib.auth import login
from django.contrib import messages


app_id = settings.SOCIAL_FACEBOOK_KEY
app_secret = settings.SOCIAL_FACEBOOK_SECRET


def get_graph():
    """Get App Graph Object.

    returns a graph object containing an app token from the registered facebook app
    """
    graph = facebook.GraphAPI(version='3.1')
    graph.access_token = graph.get_app_access_token(app_id, app_secret)
    return graph


def canv_url(request):
    """Return Canvas URL.

    Generates the canvas_url used by facebook to redirect after auth
    """
    # Check whether the last call was secure and use its protocol
    if request.is_secure():
        return 'https://' + request.get_host() + reverse('social_login:facebook_login_response')
    else:
        return 'https://' + request.get_host() + reverse('social_login:facebook_login_response')


def auth_url(request):
    """Auth URL.

    Returns the facebook auth url using the current app's domain
    """
    canvas_url = canv_url(request)

    # Permissions set by user. Default is none
    perms = settings.SOCIAL_FACEBOOK_PERMISSIONS

    url = "https://www.facebook.com/dialog/oauth?"

    # Payload
    kvps = {'client_id': app_id, 'redirect_uri': canvas_url}

    # Add 'next' as state if provided
    next_param = f"next_url={quote(request.GET.get('next', ''))}"
    # Add 'redirected' as state if provided
    redirected_param = f"redirected={request.GET.get('redirected', '')}"
    if request.GET.get('next', False):
        kvps['state'] = next_param
        redirected_param = f',{redirected_param}'
    if request.GET.get('redirected', False):
        kvps['state'] = kvps.get('state', '') + redirected_param

    # Format permissions if needed
    if perms:
        kvps['scope'] = ",".join(perms)

    # Return the url
    return url + urlencode(kvps)


def debug_token(token):
    """Debug Token.

    Returns debug string from token
    """
    return get_graph().debug_access_token(token, app_id, app_secret)


def login_successful(code, request):
    """Login Successful.

    Process successful login by creating or updating an user using Facebook's response
    """
    canvas_url = canv_url(request)
    graph = get_graph()

    # Get token info from user
    try:
        token_info = graph.get_access_token_from_code(code, canvas_url, app_id, app_secret)
    except facebook.GraphAPIError:
        # For some reason, the auth code has already been used, redirect to login again
        return 'auth code used'

    # Extract token from token info
    access_token = token_info['access_token']

    # Debug the token, as per documentation
    debug = debug_token(access_token)['data']

    # Get the user's scope ID from debug data
    social_id = debug['user_id']
    token_expires = debug.get('expires_at') - debug.get('issued_at')
    if debug.get('expires_at') == 0:
        token_expires = 99999999
    scopes = debug.get('scopes', [])

    # Get some user info like name and url
    extra_data = graph.get_object(str(social_id) + '/?fields=name,first_name,last_name,link')
    name = extra_data['name']
    first_name = extra_data['first_name']
    last_name = extra_data['last_name']
    link = extra_data.get('link', '')

    # Call FacebookUser's method to create or update based on social_id, that returns an facebookuser object
    from .models import FacebookUser
    new = FacebookUser.create_or_update(social_id, access_token, token_expires, first_name, last_name, name, link, scopes)

    # Try to login the user
    if new.user.is_active:
        login(request, new.user)
        messages.add_message(request, messages.SUCCESS, 'Olá, ' + first_name + '!')
    else:
        messages.add_message(request, messages.ERROR, 'Essa conta foi desativada!')

    return request


def login_canceled(request):

    # If the user has canceled the login process, or something else happened, do nothing and display error message
    messages.add_message(request, messages.ERROR, 'Oops! Algo de errado aconteceu :( Se isso se repetir, fale conosco!')

    return request


def decode_state_data(state):
    if not state:
        return {}
    parts = state.split(',')
    data = {}
    for part in parts:
        p = part.split('=')
        data[p[0]] = unquote(p[1])
    return data


def code_already_used_url(next_url, redirected):
    state = {}
    if next_url:
        state['next'] = next_url
    state['redirected'] = int(redirected) + 1 if redirected else 0
    return reverse('social_login:facebook_login') + '?' + urlencode(state)
