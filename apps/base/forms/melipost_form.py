from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row

from apps.base.models import Answer
from apps.base.models.meli_post import MeliPost


class MeliPostForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(MeliPostForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(FloatingField('meli_id', css_class='col-md-12'), css_class='form-group'),
            Row(FloatingField('title', css_class='col-md-12'), css_class='form-group'),
        )

    class Meta:
        model = MeliPost
        fields = '__all__'
