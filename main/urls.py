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
from custom_auth.views import FacebookLogin

urlpatterns = [
    # /+
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^login/$', FacebookLogin.as_view()),
    url(r'^about/$', views.About.as_view(), name='about'),
    url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),

    url(r'^my/$', views.MySpotteds.as_view(), name='my_spotteds'),
    url(r'^my_delete_options/$', views.MyDeleteOptions.as_view(), name='my_delete_options'),

    url(r'^for-me/$', views.ForMeSpotteds.as_view(), name='forme_spotteds'),
    url(r'^forme_delete_options/$', views.ForMeDeleteOptions.as_view(), name='forme_delete_options'),

    url(r'^delete_spotted/$', views.DeleteSpotted.as_view(), name='delete_spotted'),
    url(r'^dismiss_submit/$', views.DismissSubmit.as_view(), name='dismiss_submit'),

    url(r'^search/$', views.Search.as_view(), name='search'),

    url(r'^prefetch_facebook_users/$', views.PrefetchFacebookUsernames.as_view(), name='prefetch_facebook_users'),

    url(r'^imgur_upload/$', views.ImgurUpload.as_view(), name='upload_image'),

    url(r'^coinhive/$', views.Coinhive.as_view(), name='coinhive'),

    url(r'^coinhive_stats/$', views.GetCoinhiveStats.as_view(), name='get_coinhive_stats'),

    url(r'^get_nag/$', views.GetNagMessage.as_view(), name='get_nag_message'),
    url(r'^update_nag/$', views.UpdateNagMessage.as_view(), name='update_nag_message'),
]
