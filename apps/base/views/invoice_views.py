# Django Library
import json

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _

# Thirdparty Library
# from dal import autocomplete

# Localfolder Library
from apps.base.forms.invoice_form import InvoiceForm
from apps.base.models.invoice import Invoice
from apps.base.models.invoice import Invoice
from apps.base.views.father_view import FatherListView, FatherDetailView, FatherCreateView, FatherUpdateView, \
    FatherTableListView, FatherDeleteView

OBJECT_FIELDS = [
    {'string': _("Customer"), 'field': 'customer'},
    {'string': _("Meli Id"), 'field': 'meli_id'},
    {'string': _("Total"), 'field': 'total'},
    {'string': _("Uso de CFDI"), 'field': 'uso_cfdi'},
    {'string': _("Forma de Pago"), 'field': 'forma_pago'},
    {'string': _("Status"), 'field': 'status'},
]

OBJECT_LIST_FIELDS = [
    {'string': _("RFC"), 'field': 'customer_rfc'},
    {'string': _("ID Venta"), 'field': 'meli_id'},
    {'string': _("Total"), 'field': 'total'},
    {'string': _("Uso de CFDI"), 'field': 'get_uso_cfdi_display'},
    {'string': _("Forma de Pago"), 'field': 'get_forma_pago_display'},
    {'string': _("Status"), 'field': 'get_status_display'},
]

OBJECT_DETAIL_FIELDS = [
    {'string': _("Username"), 'field': 'customer_meli_username'},
    {'string': _("RFC"), 'field': 'customer_rfc'},
    {'string': _("Name"), 'field': 'customer_name'},
    {'string': _("CP"), 'field': 'customer_cp'},
    {'string': _("Regimen"), 'field': 'customer_regimen'},
    {'string': _("ID Venta"), 'field': 'meli_id'},
    {'string': _("Total"), 'field': 'total'},
    {'string': _("Uso de CFDI"), 'field': 'get_uso_cfdi_display'},
    {'string': _("Forma de Pago"), 'field': 'get_forma_pago_display'},
    {'string': _("Status"), 'field': 'get_status_display'},
]

OBJECT_FORM_FIELDS = [
    'customer',
    'meli_id',
    'total',
    'uso_cfdi',
    'forma_pago',
    'status',
]


# ========================================================================== #
class InvoiceListView(FatherListView):
    model = Invoice
    template_name = 'common/list.html'
    extra_context = {'fields': OBJECT_LIST_FIELDS,
                     'modal_add': True,
                     }


# ========================================================================== #
class InvoiceDetailView(FatherDetailView):
    model = Invoice
    template_name = 'invoice/detail.html'
    extra_context = {'fields': OBJECT_DETAIL_FIELDS}



# ========================================================================== #
class InvoiceCreateView(BSModalCreateView, FatherCreateView):
    model = Invoice
    # fields = OBJECT_FORM_FIELDS
    form_class = InvoiceForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: Invoice was created.'
    success_url = reverse_lazy('Invoice:list')


# # ========================================================================== #
class InvoiceDeleteView(BSModalDeleteView, FatherDeleteView):
    model = Invoice


class ProductInvoiceCreateModalView(BSModalCreateView, FatherCreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: Invoice was created.'
    success_url = reverse_lazy('Product:add')


class InvoiceUpdateView(BSModalUpdateView, FatherUpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: Invoice was updated.'


def invoices(request):
    if request.method == 'GET':
        invoices = Invoice.objects.all()
        data = {}
        for invoice in invoices:
            data[invoice.pk] = invoice.name
            data['last'] = Invoice.objects.latest('id').id
        return HttpResponse(json.dumps(data), content_type='application/json')


class InvoicesTable(FatherTableListView):
    model = Invoice
    fields = OBJECT_LIST_FIELDS


def invoice_get_id(request):
    if request.is_ajax():
        invoice_name = request.GET['invoice_name']
        invoice_id = Invoice.objects.get(name=invoice_name).id
        update_url = reverse('Invoice:update', kwargs={'pk': invoice_id})
        data = {'invoice_id': invoice_id, 'update_url': update_url}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def get_invoice_name(request):
    if request.is_ajax():
        invoice_id = request.GET['invoice_id']
        invoice_name = Invoice.objects.get(id=invoice_id).name
        data = {'invoice_name': invoice_name, }
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


# Invoice Invoice Views #
def invoice_invoice_list(request, s_pk):
    invoice = Invoice.objects.get(pk=s_pk)
    # invoice_invoices = InvoiceInvoice.objects.filter(invoice_id=invoice)
    invoice_invoices = Invoice.objects.filter(invoice_invoice__invoice_id=invoice)

    return render(request, 'invoice/invoice_invoice_list.html',
                  {'invoice': s_pk, 'invoice_name': invoice.name, 'invoice_invoices': invoice_invoices})


def invoice_invoices(request, s_pk):
    data = dict()
    if request.method == 'GET':
        invoice = Invoice.objects.get(pk=s_pk)
        invoice_invoices = Invoice.objects.filter(invoice_invoice__invoice_id=invoice)
        data['table'] = render_to_string(
            'invoice/_invoice_invoice_table.html',
            {'invoice': s_pk, 'invoice_name': invoice.name, 'invoice_invoices': invoice_invoices},
            request=request
        )
        return JsonResponse(data)
