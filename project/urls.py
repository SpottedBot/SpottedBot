from django.urls import include, path
from django.views.generic import TemplateView
from main.views import Handler404, Handler500
from django.contrib import admin
admin.autodiscover()
# from app import views

handler404 = Handler404.as_view()
handler500 = Handler500.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('custom_auth.urls', namespace='custom_auth')),
    path('spotted/', include('spotteds.urls', namespace='spotteds')),
    path('mod/', include('moderation.urls', namespace='mod')),
    path('api/', include('api.urls', namespace='api')),
    path('hooks/', include('chatbot.urls', namespace='chatbot')),

    path('robots.txt', TemplateView.as_view(template_name='main/robots.txt', content_type='text/plain')),
    path('humans.txt', TemplateView.as_view(template_name='main/humans.txt', content_type='text/plain')),

]
