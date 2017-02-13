from django.shortcuts import redirect, reverse
from .facebook_methods import auth_url, login_successful, login_canceled

# Create your views here.


def facebook_login(request):

    # Generate auth_url and redirect to it
    return redirect(auth_url(request))


def facebook_login_response(request):
    """Facebook Login Response

    Try to access 'code' from the response. If found, the login was successful. Unsuccessful otherwise
    """

    try:
        code = request.GET['code']
    except:
        # User cancelled login
        request = login_canceled(request)
        return redirect(reverse('index'))

    request = login_successful(code, request)
    return redirect(reverse('index'))
