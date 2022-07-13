from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row

from apps.base.models import Answer


class AnswerForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(FloatingField('name', css_class='col-md-12'), css_class='form-group'),
            Row(FloatingField('message', css_class='col-md-12'), css_class='form-group'),
            Row(FloatingField('context', css_class='col-md-12'), css_class='form-group'),
        )

    class Meta:
        model = Answer
        fields = '__all__'
