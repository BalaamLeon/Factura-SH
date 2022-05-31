from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field
from django import forms

from apps.base.models.sale import TrackedSale


class SaleForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_id = 'sale_form'
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(FloatingField('invoice', css_class='col-md-12')),
            Row(FloatingField('tracking', css_class='col-md-12')),
        )

    class Meta:
        model = TrackedSale
        fields = '__all__'
        labels = {
            'invoice': 'Solicitud',
            'tracking': 'Seguimiento',
        }


class SaleChatForm(BSModalForm):
    pack_id = forms.CharField(label='Pack Id')
    message = forms.CharField(label='message',
                              help_text='No incluyas datos personales, lenguaje ofensivo, links a redes sociales o '
                                        'Mercado Pago.',
                              widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Field(
                    'pack_id'
                )
            ),
            Row(
                Field(
                    'message',
                    css_class='col-md-12'
                ),
            ),
        )
