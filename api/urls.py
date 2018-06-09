"""Website URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
app_name = 'api'

urlpatterns = [
    # /api/+

    path('process_new_post/', views.ProcessNewPost.as_view(), name='process_new_post'),
    path('process_approved/', views.ProcessApproved.as_view(), name='process_approved'),
    path('process_rejected/', views.ProcessRejected.as_view(), name='process_rejected'),
    path('process_deleted/', views.ProcessDeleted.as_view(), name='process_deleted'),

    path('reject_options/', views.RejectOptions.as_view(), name='reject_options'),
    path('my_options/', views.MyDeleteOptions.as_view(), name='my_delete_options'),
    path('forme_options/', views.ForMeDeleteOptions.as_view(), name='forme_delete_options'),

    path('get_coinhive_stats/', views.CoinHiveStats.as_view(), name='coinhivestats'),

    path('chatbot/chat_submit/', views.SubmitMessageLog.as_view(), name='submit_message_log'),
    path('chatbot/process_chat_message/', views.ProcessRawBotMessage.as_view(), name='process_raw_bot_message'),
]
