from django.shortcuts import reverse
from django.views.generic import RedirectView
from .facebook_methods import auth_url, login_successful, login_canceled

# Create your views here.


class FacebookLogin(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return auth_url(self.request)


class LoginResponse(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        code = self.request.GET.get('code', False)
        next_url = self.request.GET.get('state', False)
        if not code:
            self.request = login_canceled(self.request)
        else:
            self.request = login_successful(code, self.request)
        if next_url:
            return next_url
        return reverse('index')
