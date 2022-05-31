# Django Library
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, FormView
from formtools.wizard.views import SessionWizardView

# Local folder Library
from apps.base.forms.factura_form import FacturaCustomerForm, SearchRFCForm, FacturaInvoiceForm
from apps.base.models.customer import Customer
from apps.base.models.customuser_config import UserConfig
from apps.base.models.invoice import Invoice
from apps.base.views.auth_view import check_meli_session
from apps.base.views.father_view import FatherDetailView, FatherCreateView, FatherUpdateView, \
    FatherDeleteView
from apps.meli import ApiClient, RestClientApi, ApiException

# Third party Library
from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalUpdateView

OBJECT_LIST_FIELDS = [
    {'string': _("Username"), 'field': 'meli_username'},
    {'string': _("RFC"), 'field': 'rfc'},
    {'string': _("Name"), 'field': 'name'},
    {'string': _("CP"), 'field': 'cp'},
    {'string': _("Régimen"), 'field': 'regimen'},
    {'string': _("Constancia"), 'field': 'constancia'},
]

FORMS = [("search", SearchRFCForm),
         ("customer", FacturaCustomerForm),
         ("invoice", FacturaInvoiceForm)]

TEMPLATES = {"search": "factura/search.html",
             "customer": "factura/register.html",
             "invoice": "factura/factura.html", }


class Wizard(SessionWizardView):
    file_storage = FileSystemStorage(location='constancias/')
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form_instance(self, step):
        return self.instance_dict.get(step, None)

    def done(self, form_list, **kwargs):
        # What is the exact logic to be applied here to save the model forms concurrently?
        return redirect('Factura:success')


# ========================================================================== #
class FacturaDetailView(FatherDetailView):
    model = Customer
    template_name = 'common/detail.html'
    extra_context = {'fields': OBJECT_LIST_FIELDS}


# ========================================================================== #
class SearchView(FormView):
    form_class = SearchRFCForm
    template_name = 'factura/search.html'

    def get(self, request, *args, **kwargs):
        print(self.kwargs)
        if Invoice.objects.filter(meli_id=self.kwargs['meli_sale']).exists():
            return redirect('Factura:error', meli_sale=self.kwargs['meli_sale'])
        else:
            return super(SearchView, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['meli_sale'] = self.kwargs['meli_sale']
        return context


# ========================================================================== #
def search_rfc_view(request, meli_sale):
    if request.method == "GET":
        query = request.GET.get('rfc').upper()
        if query == '':
            query = 'None'
        try:
            customer = Customer.objects.get(rfc=query)
            return redirect(reverse('Factura:update', kwargs={'pk': customer.pk, 'meli_sale': meli_sale}))
        except Customer.DoesNotExist:
            return redirect(reverse('Factura:add', kwargs={'rfc': query, 'meli_sale': meli_sale}))
    return render(request, 'factura/search.html')


# ========================================================================== #
class FacturaCustomerCreateView(FatherCreateView):
    model = Customer
    form_class = FacturaCustomerForm
    template_name = 'factura/register.html'
    success_message = 'Success: User was created.'

    def get_initial(self):
        initial = super(FacturaCustomerCreateView, self).get_initial()
        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value

            resource = 'orders/' + str(self.kwargs['meli_sale'])

            try:
                # Resource path GET
                api_response = api_instance.resource_get(resource, access_token)
                username = api_response['buyer']['nickname']
                initial['meli_username'] = username
            except ApiException as e:
                print("Exception when calling RestClientApi->resource_get: %s\n" % e)

        initial['rfc'] = self.kwargs['rfc']
        initial['regimen'] = '621'
        return initial

    def get_success_url(self):
        return reverse('Factura:invoice', args=(self.kwargs['meli_sale'], self.object.pk))


# ========================================================================== #
class FacturaCustomerDeleteView(BSModalDeleteView, FatherDeleteView):
    model = Customer


# ========================================================================== #
class FacturaCustomerUpdateView(BSModalUpdateView, FatherUpdateView):
    model = Customer
    form_class = FacturaCustomerForm
    template_name = 'factura/register.html'
    success_message = 'Success: Factura was updated.'

    def __init__(self):
        super(FacturaCustomerUpdateView, self).__init__()
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        file = self.request.FILES.get('constancia')
        print(file)
        if not file:
            print("No file")
            print(self.object.constancia)
            self.object.constancia = self.object.constancia
        self.object.save()
        return super(FacturaCustomerUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Factura:invoice', args=(self.kwargs['meli_sale'], self.object.id,))


# ========================================================================== #
class FacturaInvoiceCreateView(FatherCreateView):
    model = Invoice
    form_class = FacturaInvoiceForm
    template_name = 'factura/factura.html'
    success_message = 'Success: User was created.'
    extra_context = {'customer_fields': {'name': 'Razón Social', 'rfc': 'RFC', 'cp': 'CP', 'regimen': 'Régimen Fiscal'},
                     'invoice_fields': {'meli_id': 'ID de Compra', 'total': 'Total', 'uso_cfdi': 'Uso de CFDI',
                                        'forma_pago': 'Forma de pago'}}

    def get_initial(self):
        initial = super(FacturaInvoiceCreateView, self).get_initial()
        check_meli_session()

        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value

            resource = 'packs/' + str(self.kwargs['meli_sale'])

            try:
                # Resource path GET
                response = api_instance.resource_get(resource, access_token)
                resource = 'orders/' + str(response['orders'][0]['id'])
                response = api_instance.resource_get(resource, access_token)
            except ApiException:
                print('Exception in pack info')
                try:
                    resource = 'orders/' + str(self.kwargs['meli_sale'])
                    response = api_instance.resource_get(resource, access_token)

                except ApiException:
                    print('Exception in order info')

        total = response['paid_amount']
        initial['total'] = total
        initial['customer'] = self.kwargs['pk']
        initial['meli_id'] = self.kwargs['meli_sale']
        initial['uso_cfdi'] = 'G03'

        payment_type = response['payments'][0]['payment_type']
        if payment_type == 'account_money':
            initial['forma_pago'] = '06'
        elif payment_type == 'ticket':
            initial['forma_pago'] = '01'
        elif payment_type == 'bank_transfer' or payment_type == 'atm':
            initial['forma_pago'] = '03'
        elif payment_type == 'credit_card':
            initial['forma_pago'] = '04'
        elif payment_type == 'debit_card':
            initial['forma_pago'] = '28'
        elif payment_type == 'prepaid_card':
            initial['forma_pago'] = '05'
        else:
            initial['forma_pago'] = '01'
        return initial

    def get_context_data(self, **kwargs):
        context = super(FacturaInvoiceCreateView, self).get_context_data(**kwargs)
        context['meli_sale'] = self.kwargs['meli_sale']
        context['customer'] = Customer.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('Factura:success', kwargs={'meli_sale': self.kwargs['meli_sale']})


# ========================================================================== #
class FacturaInvoiceSuccessView(TemplateView):
    template_name = 'factura/success.html'
    form_class = FacturaInvoiceForm


# ========================================================================== #
class FacturaInvoiceErrorView(TemplateView):
    template_name = 'factura/error.html'
    # form_class = FacturaInvoiceForm
