from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()
# from app import views
from django.views.generic import TemplateView

# Disabled until bug is fixed
# handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('main.urls')),
    url(r'^auth/', include('custom_auth.urls', namespace='custom_auth')),
    url(r'^spotted/', include('spotteds.urls', namespace='spotteds')),
    url(r'^mod/', include('moderation.urls', namespace='mod')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^hooks/', include('chatbot.urls', namespace='chatbot')),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='main/robots.txt', content_type='text/plain')),
    url(r'^humans\.txt$', TemplateView.as_view(template_name='main/humans.txt', content_type='text/plain')),

]
