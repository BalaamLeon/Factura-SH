from time import time

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.shortcuts import resolve_url
from django.views import View

from apps.base.forms.login_form import LoginForm
from apps.base.models import CustomUser, Answer
from apps.base.models.customuser_config import UserConfig
from apps.meli import ApiClient, OAuth20Api, ApiException


def check_meli_session():
    now = int(time())
    expires_in = UserConfig.objects.get(key='expires_in').value
    access_time = UserConfig.objects.get(key='access_time').value
    expire_time = int(expires_in) + int(access_time)

    if now > expire_time:
        # MELI_APP = MeliApp()
        client_id = '8367847789338992'
        client_secret = 'qhTLXZ37Rt9omHx3RllnYSnNKV9SPKsl'
        refresh_token = UserConfig.objects.get(key='refresh_token').value

        # response = meli.get_refresh_token()
        response = meli_auth(client_id, client_secret, refresh_token)
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        expires_in = response['expires_in']

        access_time = int(time())
        print(access_time)
        keys = ("access_token",
                "expires_in",
                "access_time",
                "refresh_token")
        entities = (access_token,
                    expires_in,
                    access_time,
                    refresh_token)
        for i, k in enumerate(keys):
            t = UserConfig.objects.get(key=k)
            t.value = entities[i]  # change field
            t.save()  # this will update only


def meli_auth(client_id, client_secret, refresh_token):
    with ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = OAuth20Api(api_client)
        grant_type = 'refresh_token'  # str
        client_id = client_id  # Your client_id
        client_secret = client_secret  # Your client_secret
        refresh_token = refresh_token  # Your refresh_token

    try:
        # Request Access Token
        api_response = api_instance.get_token(grant_type=grant_type, client_id=client_id,
                                              client_secret=client_secret,
                                              refresh_token=refresh_token)
        print(api_response)
        return api_response
    except ApiException as e:
        print("Exception when calling OAuth20Api->get_token: %s\n" % e)


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

        check_meli_session()

        return super(UserLoginView, self).form_valid(form)


# Logout view
class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('User:login')


@receiver(post_save, sender=CustomUser)
def create_user_picks(sender, instance, created, **kwargs):
    if created:
        UserConfig.objects.create(key='meli_user_id', value='86359928')
        UserConfig.objects.create(key='site_id', value='MLM')
        UserConfig.objects.create(key='user_name', value='Itzel Angelina Delgadillo León')
        UserConfig.objects.create(key='code', value='TG-622637e56b104e001a8d2423-86359928')
        UserConfig.objects.create(key='access_token',
                                  value='APP_USR-8367847789338992-052313-c44c1d0a433d6f4329a9ffc781b5c1d4-86359928')
        UserConfig.objects.create(key='expires_in', value=21600)
        UserConfig.objects.create(key='access_time', value=1653327258)
        UserConfig.objects.create(key='refresh_token', value='TG-622637e69c44e5001bc96e75-86359928')
        UserConfig.objects.create(key='new_code', value='TG-622637e56b104e001a8d2423-86359928')
        Answer.objects.create(name='Formulario',
                              message='Puedes solicitar tu factura llenando el formulario del siguiente enlace:'
                                      '<a href="invoice_url"> Solicitud de factura </a>')
