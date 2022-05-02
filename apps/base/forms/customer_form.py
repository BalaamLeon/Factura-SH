from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row

from apps.base.models.customer import Customer


class CustomerForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_id = 'customer_form'
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(FloatingField('meli_username', css_class='col-md-12'), css_class='form-group'),
            Row(FloatingField('rfc', css_class='col-md-12'), css_class='form-group'),
            Row(FloatingField('name', css_class='col-md-12'), css_class='form-group'),
            Row(FloatingField('cp', css_class='col-md-12'), css_class='form-group'),
            Row(FloatingField('regimen', css_class='col-md-12'), css_class='form-group'),
            Row(FloatingField('constancia', css_class='col-md-12'), css_class='form-group'),
        )

    class Meta:
        model = Customer
        fields = '__all__'
