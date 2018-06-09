from django.urls import path
from . import views
app_name = 'chatbot'

urlpatterns = [
    # /custom_auth/+
    path('messenger/', views.MessengerHook.as_view(), name='messenger_hook'),
]
