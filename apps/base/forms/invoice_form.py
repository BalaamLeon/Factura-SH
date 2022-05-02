from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row

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
