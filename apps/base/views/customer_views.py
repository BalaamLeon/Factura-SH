# Django Library
import json

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _

# Localfolder Library
from apps.base.forms.customer_form import CustomerForm
from apps.base.models.customer import Customer
from apps.base.views.father_view import FatherListView, FatherDetailView, FatherCreateView, FatherUpdateView, \
    FatherTableListView, FatherDeleteView

# Thirdparty Library
# from dal import autocomplete

OBJECT_FIELDS = [
    {'string': _("Username"), 'field': 'meli_username'},
    {'string': _("RFC"), 'field': 'rfc'},
    {'string': _("Name"), 'field': 'name'},
    {'string': _("CP"), 'field': 'cp'},
    {'string': _("Régimen"), 'field': 'regimen'},
    {'string': _("Constancia"), 'field': 'constancia'},
]

OBJECT_LIST_FIELDS = [
    {'string': _("Username"), 'field': 'meli_username'},
    {'string': _("RFC"), 'field': 'rfc'},
    {'string': _("Name"), 'field': 'name'},
    {'string': _("CP"), 'field': 'cp'},
    {'string': _("Régimen"), 'field': 'regimen'},
    {'string': _("Constancia"), 'field': 'constancia'},
]

OBJECT_FORM_FIELDS = [
    'meli_username',
    'rfc',
    'name',
    'cp',
    'regimen',
    'constancia',
]


# ========================================================================== #
class CustomerListView(FatherListView):
    model = Customer
    template_name = 'common/list.html'
    extra_context = {'fields': OBJECT_LIST_FIELDS,
                     'modal_add': True,
                     }


# ========================================================================== #
class CustomerDetailView(FatherDetailView):
    model = Customer
    template_name = 'common/detail.html'
    extra_context = {'fields': OBJECT_LIST_FIELDS}


# ========================================================================== #
class CustomerCreateView(BSModalCreateView, FatherCreateView):
    model = Customer
    # fields = OBJECT_FORM_FIELDS
    form_class = CustomerForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: Customer was created.'
    success_url = reverse_lazy('Customer:list')

    # def form_valid(self, form):
    #     """If the form is valid, save the associated model."""
    #     self.object = form.save(commit=False)
    #     self.object.constancia
    #     self.object.save()
    #     form.save_m2m()
    #     return super().form_valid(form)


# # ========================================================================== #
class CustomerDeleteView(BSModalDeleteView, FatherDeleteView):
    model = Customer


class CustomerUpdateView(BSModalUpdateView, FatherUpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: Customer was updated.'
    success_url = reverse_lazy('Customer:list')


def customers(request):
    if request.method == 'GET':
        customers_objects = Customer.objects.all()
        data = {}
        for customer in customers_objects:
            data[customer.pk] = customer.name
            data['last'] = Customer.objects.latest('id').id
        return HttpResponse(json.dumps(data), content_type='application/json')


class CustomersTable(FatherTableListView):
    model = Customer
    fields = OBJECT_LIST_FIELDS


def customer_get_id(request):
    if request.is_ajax():
        customer_name = request.GET['customer_name']
        customer_id = Customer.objects.get(name=customer_name).id
        update_url = reverse('Customer:update', kwargs={'pk': customer_id})
        data = {'customer_id': customer_id, 'update_url': update_url}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def get_customer_name(request):
    if request.is_ajax():
        customer_id = request.GET['customer_id']
        customer_name = Customer.objects.get(id=customer_id).name
        data = {'customer_name': customer_name, }
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def get_customer_info(request):
    if request.is_ajax():
        customer_rfc = request.GET['rfc']
        customer = Customer.objects.filter(rfc=customer_rfc).first()
        if customer is not None:
            data = {'response': 'ok', 'name': customer.name, 'cp': customer.cp, 'regimen': customer.regimen,}
        else:
            data = {'response': 'no', }
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


# Customer Invoice Views #
def customer_invoice_list(request, s_pk):
    customer = Customer.objects.get(pk=s_pk).invoices.all()
    # customer_invoices = Invoice.objects.filter(customer_invoice__customer_id=customer)

    return render(request, 'customer/customer_invoice_list.html',
                  {'customer': s_pk, 'customer_name': customer.name, 'customer_invoices': customer.invoices.all()})


def customer_invoices(request, s_pk):
    data = dict()
    if request.method == 'GET':
        customer = Customer.objects.get(pk=s_pk)
        # customer_invoices = Invoice.objects.filter(customer_invoice__customer_id=customer)
        data['table'] = render_to_string(
            'customer/_customer_invoice_table.html',
            {'customer': s_pk, 'customer_name': customer.name, 'customer_invoices': customer.invoices.all()},
            request=request
        )
        return JsonResponse(data)
