from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()
from app import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', views.login, name='index'),
    url(r'^logout/$', views.logout),
]
