# Django Library
import json
from datetime import datetime

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
# Local folder Library
from django.views.generic import TemplateView, FormView

from apps.base.forms.invoice_form import InvoiceForm, SendCFDIForm, InvoiceStatusForm, InvoiceFromSaleForm
from apps.base.models import Customer, UserConfig, Answer
from apps.base.models.invoice import Invoice
from apps.base.models.sale import TrackedSale
from apps.base.views.auth_view import check_meli_session
from apps.base.views.father_view import FatherDetailView, FatherCreateView, FatherUpdateView, \
    FatherDeleteView
from apps.meli import ApiClient, RestClientApi, ApiException


# ========================================================================== #
class InvoiceListView(TemplateView):
    template_name = 'invoice/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.kwargs['query']
        STATUS_CHOICES = {'pending': ('1', _('Pending Invoices')),
                          'emitted': ('2', _('Invoices to send')),
                          'sent': ('3', _('Sent Invoices')),
                          'cancelled': ('4', _('Cancelled Invoices'))}
        invoices = []

        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            my_id = UserConfig.objects.get(key='meli_user_id').value

            try:
                if query == 'tracking':
                    db_invoices = Invoice.objects.filter(tracking__tracking=True)
                    context['page_title'] = _('Invoices with tracking')
                elif query == 'all':
                    db_invoices = Invoice.objects.all()
                    context['page_title'] = _('Invoices')
                else:
                    db_invoices = Invoice.objects.filter(status=STATUS_CHOICES[query][0])
                    context['page_title'] = STATUS_CHOICES[query][1]
                for invoice in db_invoices:
                    tracked_sale = invoice.tracking.first()
                    if tracked_sale is not None:
                        tracked = tracked_sale.tracking
                    else:
                        tracked = False

                    pack_id = invoice.meli_id
                    resource = 'packs/' + pack_id
                    response = None
                    messages_count = 0

                    try:
                        response = api_instance.resource_get(resource, access_token)
                        resource = 'orders/' + str(response['orders'][0]['id'])
                        response = api_instance.resource_get(resource, access_token)

                    except ApiException as e:
                        print('Exception in pack info')

                        try:
                            resource = 'orders/' + str(pack_id)
                            response = api_instance.resource_get(resource, access_token)

                        except ApiException as e:
                            print('Exception in order info')
                    conversation_status = ''
                    try:
                        msg_resource = 'messages/packs/' + str(pack_id) + '/sellers/' + my_id\
                                       + '?tag=post_sale&mark_as_read=false'
                        msg_response = api_instance.resource_get(msg_resource, access_token)

                        conversation_status = msg_response['conversation_status']['status']
                        for msg in msg_response['messages']:
                            if msg['message_date']['read'] is not None and msg["to"]["user_id"] == my_id:
                                messages_count += 1
                    except ApiException as e:
                        print('Exception in messages')

                    s = {
                        'pk': invoice.pk,
                        'status': invoice.status,
                        'tracked': tracked,
                        'pack_id': pack_id,
                        'channel': response['context']['channel'],
                        'id': response['id'],
                        'date': datetime.fromisoformat(response['date_created']),
                        'buyer_id': response['buyer']['id'],
                        'buyer_name': response['buyer']['first_name'] + ' ' + response['buyer']['last_name'],
                        'buyer_nickname': response['buyer']['nickname'],
                        'products': response['order_items'],
                        'product': {'image': None,
                                    'id': response['order_items'][0]['item']['id'],
                                    'title': response['order_items'][0]['item']['title'],
                                    'unit_price': response['order_items'][0]['unit_price'],
                                    'quantity': response['order_items'][0]['quantity'],
                                    'seller_sku': response['order_items'][0]['item']['seller_sku'],
                                    },
                        'conversation_status': conversation_status,
                        'messages_count': messages_count
                    }

                    resource = 'shipments/' + str(response['shipping']['id'])
                    try:
                        response = api_instance.resource_get(resource, access_token)
                        s['shipping_status'] = response['status']
                        s["logistic_type"] = response["logistic_type"]
                        if response['status'] == 'delivered':
                            s['date_delivered'] = datetime.fromisoformat(response['status_history']['date_delivered'])
                        elif response['status'] == 'ready_to_ship' or response['status'] == 'shipped':
                            s['date_delivered'] = datetime.fromisoformat(
                                response['shipping_option']['estimated_delivery_final']['date'])

                    except ApiException as e:
                        print("Exception in shipping info")

                    factura_resource = 'packs/' + str(pack_id) + '/fiscal_documents'
                    try:
                        factura_response = api_instance.resource_get(factura_resource, access_token)
                        s['factura'] = factura_response['fiscal_documents'][0]['filename']
                        s['factura_id'] = factura_response['fiscal_documents'][0]['id']

                    except ApiException as e:
                        pass

                    resource = 'items/' + str(s['product']['id'])
                    try:
                        response = api_instance.resource_get(resource, access_token)
                        s['product']['image'] = response['thumbnail']
                        s['product']['permalink'] = response['permalink']
                    except ApiException as e:
                        print("Exception in product info")

                    invoices.append(s)

            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)

        invoices.sort(key=lambda item: item['date'], reverse=True)
        context['invoices'] = invoices
        context['query'] = query
        return context


# ========================================================================== #
class InvoiceDetailView(FatherDetailView):
    model = Invoice
    template_name = 'invoice/modal_detail.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        pack_id = self.object.meli_id
        products = []
        shipping = 0
        total = 0

        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            resource = 'packs/' + pack_id
            try:
                response = api_instance.resource_get(resource, access_token)
                ship_id = response['shipment']['id']
                for order in response['orders']:
                    resource = 'orders/' + str(order['id'])
                    response = api_instance.resource_get(resource, access_token)
                    for item in response['order_items']:
                        item['subtotal'] = item['quantity'] * item['unit_price']
                        products.append(item)
                        total += item['quantity'] * item['unit_price']
            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)
                try:
                    resource = 'orders/' + pack_id
                    response = api_instance.resource_get(resource, access_token)
                    ship_id = response['shipping']['id']
                    for item in response['order_items']:
                        item['subtotal'] = item['quantity'] * item['unit_price']
                        products.append(item)
                        total += item['subtotal']
                except ApiException as e:
                    print("Exception when calling OAuth20Api->get_token: %s\n" % e)

            resource = 'shipments/' + pack_id + '/costs'
            try:
                response = api_instance.resource_get(resource, access_token)
                shipping = response['receiver']['cost']
                total += shipping
            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)

            context['factura'] = ''
            context['factura_id'] = ''
            factura_resource = 'packs/' + pack_id + '/fiscal_documents'
            try:
                factura_response = api_instance.resource_get(factura_resource, access_token)
                context['factura'] = factura_response['fiscal_documents'][0]['filename']
                context['factura_id'] = factura_response['fiscal_documents'][0]['id']

            except ApiException as e:
                pass

        context['products'] = products
        context['shipping'] = shipping
        context['total'] = total
        context['pack_id'] = pack_id

        return context


def set_tracking(request, id):
    invoice = Invoice.objects.get(pk=id)
    if request.is_ajax() and request.method == 'GET':
        tracked, created = TrackedSale.objects.get_or_create(invoice=invoice)
        if not created:
            tracked.tracking = False if TrackedSale.objects.get(invoice=invoice).tracking else True
            tracked.save()

        data = {'status': 'success', 'pk': str(id), 'tracking': tracked.tracking}
        return JsonResponse(data, status=200)
    else:
        data = {'status': 'error'}
        return JsonResponse(data, status=400)


def get_cfdi(request, pack_id, file_id):
    if request.method == 'GET':
        factura_resource = 'packs/' + str(pack_id) + '/fiscal_documents/' + file_id
        # print(factura_resource)
        factura_response = ''
        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            try:
                factura_response = api_instance.resource_get_file(factura_resource, access_token)
            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)

        with open(factura_response[0], 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=' + factura_response[2]['x-original-filename']
            return response


class SendCFDI(FormView):
    form_class = SendCFDIForm
    template_name = 'invoice/send_cfdi.html'
    success_url = reverse_lazy('Invoice:list', kwargs={'query': 'pending'})

    def get_initial(self):
        initial = super(SendCFDI, self).get_initial()
        initial['send_message'] = True
        initial['message'] = Answer.objects.get(name='Adjuntada').message
        invoice = Invoice.objects.get(pk=self.kwargs['id'])
        initial['pack_id'] = invoice.meli_id
        initial['invoice_id'] = self.kwargs['id']
        return initial

    def form_valid(self, form):
        files = self.request.FILES.getlist('files')
        pack_id = form.cleaned_data['pack_id']
        invoice = Invoice.objects.get(pk=form.cleaned_data['invoice_id'])
        invoice.status = '3'
        invoice.save()

        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            resource = 'packs/' + pack_id + '/fiscal_documents'
            fiscal_docs = {}
            for file in files:
                fiscal_docs[file.name] = (file.name, file, file.content_type)
            try:
                # Resource path GET
                api_response = api_instance.resource_post(resource, access_token, {'fiscal_document': fiscal_docs})
                print(api_response)

            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)

        # url = 'https://api.mercadolibre.com/packs/' + pack_id + '/fiscal_documents'
        # headers = {"Authorization": "Bearer " + access_token}
        # fiscal_docs = {}
        # for file in files:
        #     fiscal_docs[file.name] = (file.name, file, file.content_type)
        # r = requests.post(url, data={'fiscal_document':fiscal_docs}, headers=headers)

        return super(SendCFDI, self).form_valid(form)


# ========================================================================== #
class InvoiceCreateView(BSModalCreateView, FatherCreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: Invoice was created.'
    success_url = reverse_lazy('Invoice:list', kwargs={'query': 'pending'})


# ========================================================================== #
class InvoiceFromSaleCreateView(BSModalCreateView, FatherCreateView):
    model = Invoice
    form_class = InvoiceFromSaleForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: Invoice was created.'
    success_url = reverse_lazy('Invoice:list', kwargs={'query': 'pending'})
    extra_context = {'js_files': ['dist/js/invoice_from_sale.js']}

    def get_initial(self):
        initial = super(InvoiceFromSaleCreateView, self).get_initial()
        pack_id = self.kwargs['id']
        initial['meli_id'] = pack_id

        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value

            resource = 'packs/' + pack_id

            try:
                # Resource path GET
                response = api_instance.resource_get(resource, access_token)
                resource = 'orders/' + str(response['orders'][0]['id'])
                response = api_instance.resource_get(resource, access_token)
            except ApiException as e:
                print('Exception in pack info')
                try:
                    resource = 'orders/' + pack_id
                    response = api_instance.resource_get(resource, access_token)

                except ApiException as e:
                    print('Exception in order info')

        initial['meli_username'] = response['buyer']['nickname']

        total = response['paid_amount']
        initial['total'] = total
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

        customer = Customer.objects.filter(meli_username=response['buyer']['nickname']).first()
        if customer is not None:
            initial['rfc'] = customer.rfc
            initial['name'] = customer.name
            initial['cp'] = customer.cp
            initial['regimen'] = customer.regimen

        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        meli_username = form.cleaned_data['meli_username']
        rfc = form.cleaned_data['rfc']
        name = form.cleaned_data['name']
        cp = form.cleaned_data['cp']
        regimen = form.cleaned_data['regimen']

        customer, created = Customer.objects.get_or_create(rfc=rfc)
        customer.meli_username = meli_username
        customer.rfc = rfc
        customer.name = name
        customer.cp = cp
        customer.regimen = regimen
        customer.save()
        self.object.customer = customer
        self.object.save()
        return super(InvoiceFromSaleCreateView, self).form_valid(form)

    def form_invalid(self, form):
        # Add action to invalid form phase
        messages.success(self.request, 'An error occured while processing the payment')
        return self.render_to_response(self.get_context_data(form=form))


# # ========================================================================== #
class InvoiceDeleteView(BSModalDeleteView, FatherDeleteView):
    model = Invoice

    def get_success_url(self):
        return reverse_lazy('Invoice:list', kwargs={'query': self.kwargs['query']})


class ProductInvoiceCreateModalView(BSModalCreateView, FatherCreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: Invoice was created.'
    success_url = reverse_lazy('Product:add')


class change_status(BSModalUpdateView, FatherUpdateView):
    model = Invoice
    form_class = InvoiceStatusForm
    template_name = 'common/modal_update_form.html'
    success_message = 'Success: Invoice was updated.'


def invoices(request):
    if request.method == 'GET':
        invoices = Invoice.objects.all()
        data = {}
        for invoice in invoices:
            data[invoice.pk] = invoice.name
            data['last'] = Invoice.objects.latest('id').id
        return HttpResponse(json.dumps(data), content_type='application/json')


class InvoicesTable(TemplateView):
    template_name = 'invoice/_table_list.html'

    def get(self, request, *args, **kwargs):
        query = self.kwargs['query']
        STATUS_CHOICES = {'pending': '1',
                          'emitted': '2',
                          'sent': '3',
                          'cancelled': '4'}
        invoices = []

        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            my_id = UserConfig.objects.get(key='meli_user_id').value

            try:
                db_invoices = Invoice.objects.filter(status=STATUS_CHOICES[query])
                for invoice in db_invoices:
                    pack_id = invoice.meli_id
                    resource = 'packs/' + pack_id
                    response = None
                    messages_count = 0

                    try:
                        response = api_instance.resource_get(resource, access_token)
                        resource = 'orders/' + str(response['orders'][0]['id'])
                        response = api_instance.resource_get(resource, access_token)

                    except ApiException as e:
                        print('Exception in pack info')

                        try:
                            resource = 'orders/' + pack_id
                            response = api_instance.resource_get(resource, access_token)

                        except ApiException as e:
                            print('Exception in order info')

                    try:
                        msg_resource = 'messages/packs/' + str(pack_id) + '/sellers/' + my_id + '?tag=post_sale&mark_as_read=false'
                        msg_response = api_instance.resource_get(msg_resource, access_token)

                        conversation_status = msg_response['conversation_status']['status']
                        for msg in msg_response['messages']:
                            if msg['message_date']['read'] is not None and msg["to"]["user_id"] == my_id:
                                messages_count += 1
                    except ApiException as e:
                        print('Exception in messages')

                    s = {
                        'pk': invoice.pk,
                        'pack_id': pack_id,
                        'channel': response['context']['channel'],
                        'id': response['id'],
                        'date': datetime.fromisoformat(response['date_created']),
                        'buyer_id': response['buyer']['id'],
                        'buyer_name': response['buyer']['first_name'] + ' ' + response['buyer']['last_name'],
                        'buyer_nickname': response['buyer']['nickname'],
                        'products': response['order_items'],
                        'product': {'image': None,
                                    'id': response['order_items'][0]['item']['id'],
                                    'title': response['order_items'][0]['item']['title'],
                                    'unit_price': response['order_items'][0]['unit_price'],
                                    'quantity': response['order_items'][0]['quantity'],
                                    'seller_sku': response['order_items'][0]['item']['seller_sku'],
                                    },
                        'conversation_status': conversation_status,
                        'messages_count': messages_count
                    }

                    resource = 'shipments/' + str(response['shipping']['id'])
                    try:
                        response = api_instance.resource_get(resource, access_token)
                        s['shipping_status'] = response['status']
                        s["logistic_type"] = response["logistic_type"]
                        if response['status'] == 'delivered':
                            s['date_delivered'] = datetime.fromisoformat(response['status_history']['date_delivered'])
                        elif response['status'] == 'ready_to_ship' or response['status'] == 'shipped':
                            s['date_delivered'] = datetime.fromisoformat(
                                response['shipping_option']['estimated_delivery_final']['date'])

                    except ApiException as e:
                        print("Exception in shipping info")

                    resource = 'items/' + str(s['product']['id'])
                    try:
                        response = api_instance.resource_get(resource, access_token)
                        s['product']['image'] = response['thumbnail']
                        s['product']['permalink'] = response['permalink']
                    except ApiException as e:
                        print("Exception in product info")

                    invoices.append(s)

            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)

        invoices.sort(key=lambda item: item['date'], reverse=True)

        data = dict()
        data['table'] = render_to_string(
            'invoice/_list_table.html',
            {'invoices': invoices},
        )
        return JsonResponse(data, status=200, safe=False)


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
