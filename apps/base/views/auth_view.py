from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout, authenticate
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import resolve_url, render
from django.views import View
from django.shortcuts import redirect

from apps.base.forms.login_form import LoginForm


class UserLoginView(LoginView):
    authentication_form = LoginForm
    form_class = LoginForm
    redirect_authenticated_user = False
    template_name = 'auth/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url('base:dashboard')

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        login(self.request, form.get_user())

        if remember_me:
            self.request.session.set_expiry(1209600)
        return super(UserLoginView, self).form_valid(form)


# Logout view
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('User:login')
