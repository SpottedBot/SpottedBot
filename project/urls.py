from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()
# from app import views
from django.views.generic import TemplateView

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('main.urls')),
    url(r'^auth/', include('custom_auth.urls', namespace='custom_auth')),
    url(r'^spotted/', include('spotteds.urls', namespace='spotteds')),
    url(r'^mod/', include('moderation.urls', namespace='mod')),
    url(r'^api/', include('api.urls', namespace='api')),
    # url(r'^$', views.index, name='index'),
    # url(r'^logout/$', views.logout),

    # url(r'^post_spotted/$', views.post_spotted, name='post_spotted'),
    # url(r'^delete_spotted/$', views.delete_spotted),
    # url(r'^dismiss_spotted/$', views.dismiss_spotted),
    # url(r'^report_spotted/$', views.report_spotted),
    # url(r'^unspam_spotted/$', views.unspam_spotted),
    # url(r'^mod/$', views.moderation),
    # url(r'^profile/$', views.profile),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^humans\.txt$', TemplateView.as_view(template_name='humans.txt', content_type='text/plain')),

]
