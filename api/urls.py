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
from django.conf.urls import url
from . import views
app_name = 'api'

urlpatterns = [
    # /api/+

    url(r'process_new_post/$', views.ProcessNewPost.as_view(), name='process_new_post'),
    url(r'process_approved/$', views.ProcessApproved.as_view(), name='process_approved'),
    url(r'process_rejected/$', views.ProcessRejected.as_view(), name='process_rejected'),
    url(r'process_deleted/$', views.ProcessDeleted.as_view(), name='process_deleted'),

    url(r'reject_options/$', views.RejectOptions.as_view(), name='reject_options'),
    url(r'my_options/$', views.MyDeleteOptions.as_view(), name='my_delete_options'),
    url(r'forme_options/$', views.ForMeDeleteOptions.as_view(), name='forme_delete_options'),

    url(r'get_coinhive_stats/$', views.CoinHiveStats.as_view(), name='coinhivestats'),

    url(r'chatbot/chat_submit/$', views.SubmitMessageLog.as_view(), name='submit_message_log'),
    url(r'chatbot/process_chat_message/$', views.ProcessRawBotMessage.as_view(), name='process_raw_bot_message'),
]
