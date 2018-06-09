from .decorators import messenger_enabled, messenger_secure
from .handler import handler
import json

from django.http import HttpResponse
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied


@method_decorator([messenger_enabled, csrf_exempt], name='dispatch')
class MessengerHook(View):

    def get(self, request, *args, **kwargs):
        if request.GET.get('hub.verify_token', False) == settings.FACEBOOK_VERIFY_CHATBOT:
            return HttpResponse(self.request.GET['hub.challenge'])
        raise PermissionDenied

    @method_decorator(messenger_secure)
    def post(self, request, *args, **kwargs):
        messages = json.loads(self.request.body.decode('utf-8')).get('entry', None)
        handler(messages)
        return HttpResponse()
