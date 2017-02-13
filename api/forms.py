from django import forms
import requests
from django.conf import settings


url = settings.SPOTTED_API_URL


class TokenForm(forms.Form):
    """Token Form

    Form used by the site admin when recovering their token. Deprecated
    """

    username = forms.CharField(label='Usuário', max_length=100)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(), max_length=100)

    def check(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        data = {
            'username': username,
            'password': password
        }
        response = requests.post(url, data=data)

        if not response.status_code == requests.codes.ok:
            return False

        return response.json()
