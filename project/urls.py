from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()
from app import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout),

    url(r'^post_spotted/$', views.post_spotted),
    url(r'^delete_spotted/$', views.delete_spotted),
    url(r'^dismiss_spotted/$', views.dismiss_spotted),
    url(r'^report_spotted/$', views.report_spotted),
    url(r'^unspam_spotted/$', views.unspam_spotted),
    url(r'^mod/$', views.moderation),
    url(r'^profile/$', views.profile),

]
