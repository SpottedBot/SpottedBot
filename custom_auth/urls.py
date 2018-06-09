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
from django.urls import path
from django.contrib.auth.views import logout
from . import views
app_name = 'custom_auth'

urlpatterns = [
    # /custom_auth/+
    path('facebook/login/', views.FacebookLogin.as_view(), name='facebook_login'),
    path('facebook/login_response/', views.LoginResponse.as_view(), name='facebook_login_response'),
    path('logout/', logout, {'next_page': '/'}, name='logout'),
]
