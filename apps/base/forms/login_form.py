from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from apps.base.forms.custom_fields import CustomFloatingFieldWithIcon


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.include_media = False
        self.helper.layout = Layout(
            Row(
                CustomFloatingFieldWithIcon('username', icon='fa-user'),

            ),
            Row(
                CustomFloatingFieldWithIcon('password', icon='fa-lock'),
            ),
        )

    # class Meta:
    #     fields = ['username', 'password', 'remember_me', 'submit']

    class Media:
        js = ('dist/js/pages/bootstrap5_form_validation.js',)

    remember_me = forms.BooleanField(required=False)
