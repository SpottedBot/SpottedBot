from django.conf.urls import url
from . import views
app_name = 'chatbot'

urlpatterns = [
    # /custom_auth/+
    url(r'messenger/$', views.MessengerHook.as_view(), name='messenger_hook'),
]
