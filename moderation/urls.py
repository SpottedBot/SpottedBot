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
from . import views
app_name = 'moderation'

urlpatterns = [
    # /mod/+

    path('pending/', views.PendingSpottedsView.as_view(), name='pending'),
    path('polemic/', views.PolemicSpottedsView.as_view(), name='polemic'),
    path('history/', views.HistorySpottedsView.as_view(), name='history'),
    path('reported/', views.ReportedSpottedsView.as_view(), name='reported'),
    path('change_shifts/', views.ChangeShifts.as_view(), name='shifts'),
    path('show_shifts/', views.ShowShifts.as_view(), name='show_shifts'),
    path('polemic_submit/', views.PolemicSubmit.as_view(), name='polemic_submit'),
    path('approve_submit/', views.ApproveSubmit.as_view(), name='approve_submit'),
    path('reject_options/', views.RejectOptions.as_view(), name='reject_options'),
    path('reject_submit/', views.RejectSubmit.as_view(), name='reject_submit'),
    path('un_report_submit/', views.UnReportSubmit.as_view(), name='un_report_submit'),
    path('report_submit/', views.ReportSubmit.as_view(), name='report_submit'),
]
