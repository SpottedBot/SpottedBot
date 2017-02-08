from django.shortcuts import redirect, reverse
from .facebook_methods import auth_url, login_successful, login_canceled

# Create your views here.


def facebook_login(request):
    return redirect(auth_url(request))


def facebook_login_response(request):
    try:
        request = login_successful(request.GET['code'], request)
    except:
        # User cancelled login
        request = login_canceled(request)

    return redirect(reverse('index'))
