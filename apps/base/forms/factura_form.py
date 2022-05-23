from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, HTML, Submit, Column, Field
from django import forms
from django.forms import models

from apps.base.forms.custom_fields import PrependedText
from apps.base.models.customer import Customer
from apps.base.models.invoice import Invoice


class SearchRFCForm(models.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SearchRFCForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'search_form'
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(FloatingField('rfc', css_class='col-md-12'), css_class='form-group'),
        )

    class Meta:
        model = Customer
        fields = ['rfc']
        labels = {'rfc': 'RFC'}


class FacturaCustomerForm(models.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FacturaCustomerForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_id = 'factura_form'
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(
                Column(FloatingField('rfc'), css_class='col-md-6'),
                Column(FloatingField('meli_username'),
                       Div(HTML('''{% load static %}
                                    <a class="img-tooltip">
                                        <i class="fa fa-question-circle"></i>
                                        <span>
                                            Ingresa el nombre de usuario con el que inicias sesión en MercadoLibre
                                        </span>
                                    </a>
                                    '''), css_class='help-tooltip'),
                       css_class='col-md-6'),
            ),
            Row(FloatingField('name', css_class='col-md-12')),
            Row(
                Column(FloatingField('cp'), css_class='col-md-6'),
                Column(FloatingField('regimen'), css_class='col-md-6')
            ),
            Row(Field('constancia', css_class='col-md-12'),
                Div(HTML('''{% load static %}
                            <a class="img-tooltip">
                                <i class="fa fa-question-circle"></i>
                                <span>
                                    Por disposición oficial y para cumplir con la versión 4.0 de facturación requerida
                                    por el SAT, es necesario que nos proporciones tu Constancia de Situación Fiscal.
                                    En caso contrario no podremos emitir tu factura.
                                    <br>Solo se aceptan archivos PDF.
                                </span>
                            </a>
                            '''), css_class='help-tooltip', style='top: -8.7rem; right: -15rem;'),
                )
        )

    class Meta:
        model = Customer
        fields = '__all__'
        labels = {
            "rfc": "RFC",
            "meli_username": "Usuario de Mercado Libre",
            "name": "Nombre o Razón Social",
            "regimen": "Régimen Fiscal",
            "cp": "Código Postal",
            "constancia": "Constancia de Situación Fiscal",
        }
        widgets = {
            'regimen': forms.Select(attrs={'class': 'form-control'}),
            'constancia': forms.ClearableFileInput(attrs={'accept': '.pdf'}),
        }


class FacturaInvoiceForm(models.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FacturaInvoiceForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_id = 'factura_form'
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(FloatingField('customer', css_class='col-md-12')),
            Row(
                Column(
                    FloatingField('meli_id'),
                    Div(HTML('''
                        {% load static %}
                        <a class="img-tooltip">
                            <i class="fa fa-question-circle"></i>
                            <span>
                                Es importante que el ID de la compra de Mercado Libre sea correcto, ya que será ahí donde adjuntaremos tu factura.
                                <br>Lo puedes encontrar en la página del detalle de la compra.
                                <img src="{% static 'img/id-compra-help.jpg' %}" />
                            </span>
                        </a>
                        '''),
                        css_class='help-tooltip'),
                    css_class='col-md-6'),
                Column(
                    FloatingField('total'),
                    Div(
                        HTML('''
                        {% load static %}
                        <a class="img-tooltip">
                            <i class="fa fa-question-circle"></i>
                            <span>
                                Ingresa el total de tu compra.<br>
                                Incluyendo el envío.
                                <img src="{% static 'img/total-help.jpg' %}" />
                            </span>
                        </a>
                        '''),
                        css_class='help-tooltip'),
                    css_class='col-md-6')
            ),
            Row(
                Column(
                    FloatingField('uso_cfdi'),
                    css_class='col-md-6'
                ),
                Column(
                    FloatingField('forma_pago'),
                    css_class='col-md-6'
                )
            ),
            Row(
                FloatingField('status', css_class='col-md-12')
            ),
        )

    class Meta:
        model = Invoice
        fields = '__all__'
        labels = {
            "customer": "RFC Cliente",
            "meli_id": "ID de compra en Mercado Libre",
            "total": "Total de la compra",
            "uso_cfdi": "Uso de CFDI",
            "forma_pago": "Forma de pago",
            "status": "Estatus de la factura",
        }
        widgets = {
            'customer': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'total': forms.NumberInput(
                attrs={'data-type': 'currency', 'type': "text", 'pattern': "^\$\d{1,3}(,\d{3})*(\.\d+)?$"})
        }
