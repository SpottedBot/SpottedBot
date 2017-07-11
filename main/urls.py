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

urlpatterns = [
    # /+
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    url(r'^contact/$', views.contact, name='contact'),
    url(r'^report/$', views.report, name='report'),

    url(r'^my/$', views.my_spotteds, name='my_spotteds'),
    url(r'^my_delete_options/$', views.my_delete_options, name='my_delete_options'),

    url(r'^for-me/$', views.forme_spotteds, name='forme_spotteds'),
    url(r'^forme_delete_options/$', views.forme_delete_options, name='forme_delete_options'),

    url(r'^delete_spotted/$', views.delete_spotted, name='delete_spotted'),
    url(r'^dismiss_submit/$', views.dismiss_submit, name='dismiss_submit'),

    url(r'^search/$', views.search, name='search'),

    url(r'^prefetch_facebook_users/$', views.prefetch_facebook_usernames, name='prefetch_facebook_users'),

    url(r'^imgur_upload/$', views.imgur_image_upload, name='upload_image'),
]
