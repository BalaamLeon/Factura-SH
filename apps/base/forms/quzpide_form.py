from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML
from django.forms import models

from apps.base.models.quzpide import QuzpideSale


class QuzpideDesignForm(models.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(QuzpideDesignForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_id = 'factura_form'
        self.helper.form_tag = False
        # self.helper.include_media = False
        self.helper.layout = Layout(
            Row(
                Column(
                    FloatingField('meli_username'),
                    css_class='col-md-6'),
                Column(
                    FloatingField('meli_sale'),
                    css_class='col-md-6'),
            ),

            Row(HTML('''
                            <div class="formColumn form-group col-md-12 image-uploader-container">
                            
                                <div class="fileUpload btn btn-info form-group col-md-12">
                                    <span>Select Files</span>
                                    <input id="add_img_btn" type="file" class="upload" multiple="multiple"
                                           accept=".jpg, .jpeg, .pdf"/>
                                </div>
                                <ul id="p_images">
                                </ul>
                            </div>
                            '''), css_class='form-group'),
        )

    class Meta:
        model = QuzpideSale
        fields = '__all__'
        labels = {
            "meli_username": "Usuario",
            "meli_sale": "ID de compra en Mercado Libre",
            "design_files": "Archivo(s)",
        }
