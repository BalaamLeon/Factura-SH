# Django Library
from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .father_view import (FatherCreateView, FatherDeleteView, FatherDetailView, FatherListView, FatherUpdateView)
# Localfolder Library
from ..forms.customuser_config_form import CustomUserConfigForm
from ..models.customuser_config import UserConfig

OBJECT_LIST_FIELDS = [
    {'string': _("Key"), 'field': 'key'},
    {'string': _("Value"), 'field': 'value'},
]

OBJECT_FORM_FIELDS = ['key', 'value']


class ParameterListView(FatherListView):
    model = UserConfig
    template_name = 'common/list.html'
    extra_context = {'fields': OBJECT_LIST_FIELDS,
                     'modal_add': True,}


class ParameterDetailView(FatherDetailView):
    model = UserConfig
    template_name = 'common/detail.html'
    extra_context = {'fields': OBJECT_LIST_FIELDS}


class ParameterCreateView(BSModalCreateView, FatherCreateView):
    model = UserConfig
    form_class = CustomUserConfigForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: Param was created.'
    success_url = reverse_lazy('UserConfig:list')


class ParameterUpdateView(FatherUpdateView):
    model = UserConfig
    fields = OBJECT_FORM_FIELDS
    template_name = 'common/form.html'


class ParameterDeleteView(FatherDeleteView):
    model = UserConfig
