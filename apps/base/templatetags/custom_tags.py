from django import template
from django.template.defaultfilters import safe

# from apps.base.models import CustomUser
# from apps.base.models.base_config import BaseConfig
# from apps.base.models.product import Product

register = template.Library()


@register.filter
def get_obj_attr(obj, attr):
    attribute = getattr(obj, attr)
    if callable(attribute):
        return attribute()
    return attribute

@register.simple_tag
def page_header(title):
    output = '''
        <div class="content-header">
            <div class="container-fluid">
                <div class="row mb-2">
                    <div class="col-sm-6">
                        <h1 class="m-0">''' + title + '''</h1>
                    </div><!-- /.col -->
                    <div class="col-sm-6">
                        {% render_breadcrumbs %}
        
                    </div><!-- /.col -->
                </div><!-- /.row -->
            </div><!-- /.container-fluid -->
        </div>
    '''
    return safe(output)
