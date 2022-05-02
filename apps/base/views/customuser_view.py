# -*- coding: utf-8 -*-
"""
Vistas de la aplicación globales
"""

# Thirdparty Library
import requests
# Django Library
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .father_view import (
    FatherCreateView)
# ========================================================================== #
from ..forms.signup_form import RegisterForm
from ..models.customuser import CustomUser


# Localfolder Library


class LogOutModalView(TemplateView):
    """Lista de las ordenes de venta
    """
    template_name = 'usercustom/logoutmodal.html'


##############################################################################
class SignUpView(FatherCreateView):
    """Esta clase sirve registrar a los usuarios en el sistema
    """
    model = CustomUser
    form_class = RegisterForm
    template_name = 'auth/signup.html'
    extra_context = {}
    success_url = 'CustomUser:login'
    success_message = _(
        'Your account was created successfully.')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None
        form = self.get_form()
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = requests.get(url, params=values, verify=True)
        result = data.json()

        if form.is_valid() and result['success']:
            self.extra_context['reCAPTCHA_error'] = ''
            return self.form_valid(form)
        else:
            if not result['success']:
                self.extra_context['reCAPTCHA_error'] = _('Invalid reCAPTCHA')
            return self.form_invalid(form)