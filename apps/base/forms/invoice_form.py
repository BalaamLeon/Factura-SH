from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field, Column
from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.base.models import Customer
from apps.base.models.invoice import Invoice


class InvoiceForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_id = 'invoice_form'
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(FloatingField('customer', css_class='col-md-12')),
            Row(FloatingField('meli_id', css_class='col-md-12')),
            Row(FloatingField('total', css_class='col-md-12')),
            Row(FloatingField('uso_cfdi', css_class='col-md-12')),
            Row(FloatingField('forma_pago', css_class='col-md-12')),
            Row(FloatingField('status', css_class='col-md-12')),
        )

    class Meta:
        model = Invoice
        fields = '__all__'
        labels = {
            'customer': 'Cliente',
            'meli_id': 'ID de venta en Mercado Libre',
            'total': 'Total de la venta',
            'uso_cfdi': 'Uso de CFDI',
            'forma_pago': 'Forma de pago',
            'status': 'Estado'
        }


class InvoiceStatusForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(InvoiceStatusForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_id = 'invoice_form'
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(FloatingField('status', css_class='col-md-12')),
        )

    class Meta:
        model = Invoice
        fields = ['status', ]
        labels = {
            'status': 'Estado'
        }


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.xml']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension. Only .pdf and .xml files allowed.'))


class SendCFDIForm(forms.Form):
    files = forms.FileField(label=_('Select CFDI files.'),
                            widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': '.pdf, .xml'}),
                            validators=[validate_file_extension])
    send_message = forms.BooleanField(label=_('Send message to buyer.'), required=False)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea())
    pack_id = forms.CharField(widget=forms.HiddenInput())
    invoice_id = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(SendCFDIForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_id = 'send_cfdi_form'
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(FloatingField('files', css_class='col-md-12')),
            Field('send_message', css_class='col-md-12'),
            Row(FloatingField('message', css_class='col-md-12'), css_class='send_cfdi_message'),
            Row(FloatingField('pack_id', css_class='col-md-12')),
            Row(FloatingField('invoice_id', css_class='col-md-12')),
        )


def regimen_options():
    return Customer._meta.get_field('regimen').choices


class InvoiceFromSaleForm(BSModalModelForm):
    meli_username = forms.CharField(label='Meli Username')
    rfc = forms.CharField(label='RFC')
    name = forms.CharField(label='Customer Name')
    cp = forms.CharField(label='CP')
    regimen = forms.CharField(label='Régimen',
                              widget=forms.Select(choices=regimen_options(), attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(InvoiceFromSaleForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_id = 'invoice_form'
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(FloatingField('meli_username', css_class='col-md-12')),
                    Row(FloatingField('rfc', css_class='col-md-12')),
                    Row(FloatingField('name', css_class='col-md-12')),
                    Row(FloatingField('cp', css_class='col-md-12')),
                    Row(FloatingField('regimen', css_class='col-md-12')),
                ),
                Column(
                    # Row(FloatingField('customer', css_class='col-md-12')),
                    Row(FloatingField('meli_id', css_class='col-md-12')),
                    Row(FloatingField('total', css_class='col-md-12')),
                    Row(FloatingField('uso_cfdi', css_class='col-md-12')),
                    Row(FloatingField('forma_pago', css_class='col-md-12')),
                    Row(FloatingField('status', css_class='col-md-12')),
                )
            )
        )

    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ('customer',)
        labels = {
            'customer': 'Cliente',
            'meli_id': 'ID de venta en Mercado Libre',
            'total': 'Total de la venta',
            'uso_cfdi': 'Uso de CFDI',
            'forma_pago': 'Forma de pago',
            'status': 'Estado'
        }
