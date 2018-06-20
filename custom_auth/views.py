from django.shortcuts import reverse
from django.views.generic import RedirectView
from .facebook_methods import auth_url, login_successful, login_canceled, decode_state_data, code_already_used_url

# Create your views here.


class FacebookLogin(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return auth_url(self.request)


class LoginResponse(RedirectView):
    max_code_redirects = 3

    def get_redirect_url(self, *args, **kwargs):
        code = self.request.GET.get('code', False)
        state_data = decode_state_data(self.request.GET.get('state', False))
        redirected = state_data.get('redirected', False)
        next_url = state_data.get('next_url', False)
        if not code or redirected and int(redirected) >= self.max_code_redirects:
            self.request = login_canceled(self.request)
            return reverse('index')
        else:
            response = login_successful(code, self.request)
            if response == 'auth code used':
                # if the auth code has already been used, redirect
                return code_already_used_url(next_url, redirected)
            self.request = response
        if next_url:
            return next_url
        return reverse('index')
