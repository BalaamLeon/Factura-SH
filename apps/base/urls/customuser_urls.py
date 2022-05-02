# Django Library
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

# Localfolder Library
from apps.base.views.auth_view import UserLoginView
from apps.base.views.customuser_view import SignUpView, LogOutModalView

app_name = 'CustomUser'

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path(
        'login/',
        UserLoginView.as_view(
            template_name='auth/login.html',
            # redirect_field_name='next',
            success_url='home'
        ),
        name='login'),
    path(
        'logout',
        LogoutView.as_view(next_page='PyUser:login'),
        name='logout'
    ),
    path('logoutmodal/', LogOutModalView.as_view(), name='logout-modal'),
]