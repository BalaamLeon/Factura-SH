from datetime import datetime

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


@register.filter
def get_date_from_str(value):
    months = ['ene', 'feb', 'mar', 'abr', 'may', 'jun',
              'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
    return value[8:10] + ' de ' + months[int(value[5:7]) + 1] + ' - ' + value[11:16]


@register.filter
def get_sale_status(value):
    status = ''
    if value == 'handling':
        status = 'En preparación'
    elif value == 'shipped':
        status = 'En camino'
    elif value == 'delivered':
        status = 'Entregado'
    elif value == 'ready_to_ship':
        status = 'Listo para enviar'
    return status
