"""website URL Configuration

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
app_name = 'moderation'

urlpatterns = [
    # /mod/+

    url(r'pending/$', views.pending_spotteds, name='pending'),
    url(r'polemic/$', views.polemic_spotteds, name='polemic'),
    url(r'history/$', views.history_spotteds, name='history'),
    url(r'reported/$', views.reported_spotteds, name='reported'),
    url(r'change_shifts/$', views.change_shifts, name='shifts'),
    url(r'show_shifts/$', views.show_shifts, name='show_shifts'),
    url(r'polemic_submit/$', views.polemic_submit, name='polemic_submit'),
    url(r'approve_submit/$', views.approve_submit, name='approve_submit'),
    url(r'reject_options/$', views.reject_options, name='reject_options'),
    url(r'reject_submit/$', views.reject_submit, name='reject_submit'),
    url(r'un_report_submit/$', views.un_report_submit, name='un_report_submit'),
    url(r'report_submit/$', views.report_submit, name='report_submit'),
]
