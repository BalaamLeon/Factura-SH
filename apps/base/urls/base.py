from django.conf.urls import url
from django.urls import path, include

from django.contrib.auth import views as auth_views

from apps.base.views.auth_view import UserLoginView
from apps.base.views.dashboard_view import Dashboard

app_name = 'base'

urlpatterns = [
    path('', UserLoginView.as_view(), name='home'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),

]
