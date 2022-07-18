# Django Library

# Thirdparty Library
import json
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from apps.base.models import Answer, Invoice
from apps.base.models.customuser_config import UserConfig
from apps.base.views.auth_view import check_meli_session
from apps.meli import ApiException, RestClientApi, ApiClient


# Localfolder Library


# ========================================================================== #
class SaleListView(TemplateView):
    template_name = 'sales/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.kwargs['query']
        sales = []

        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            my_id = UserConfig.objects.get(key='meli_user_id').value

            meli_sales = []
            try:
                if query == 'new_messages':
                    context['page_title'] = _('Sales with new messages')
                    resource = 'messages/unread?tag=post_sale&role=seller'
                    api_response = api_instance.resource_get(resource, access_token)
                    for sale in api_response['results']:
                        if sale['resource'].split('/')[4] == UserConfig.objects.get(key="meli_user_id").value:
                            pack_id = sale['resource'].split('/')[2]
                            meli_sales.append(str(pack_id))
                elif query == 'all':
                    context['page_title'] = _('Recent sales')
                    resource = 'orders/search/recent?seller=' + my_id + '&limit=10&sort=date_desc'
                    api_response = api_instance.resource_get(resource, access_token)
                    for sale in api_response['results']:
                        pack_id = sale['id']
                        meli_sales.append(str(pack_id))

                for pack_id in meli_sales:

                    try:
                        invoice = Invoice.objects.get(meli_id=pack_id)
                    except Invoice.DoesNotExist:
                        invoice = None
                    resource = 'packs/' + pack_id
                    response = None
                    messages_count = 0
                    conversation_status = 'blocked'

                    try:
                        response = api_instance.resource_get(resource, access_token)
                        order_id = str(response['orders'][0]['id'])
                        resource = 'orders/' + order_id
                        response = api_instance.resource_get(resource, access_token)
                    except ApiException as e:
                        print('Exception in pack info')
                        try:
                            order_id = pack_id
                            resource = 'orders/' + order_id
                            response = api_instance.resource_get(resource, access_token)
                            pack_id = str(response['pack_id'])

                        except ApiException as e:
                            print('Exception in order info')

                    try:
                        msg_resource = 'messages/packs/' + str(order_id if pack_id == "None" else pack_id) + '/sellers/' \
                                       + my_id + '?tag=post_sale&mark_as_read=false'
                        msg_response = api_instance.resource_get(msg_resource, access_token)
                        print(msg_response)

                        conversation_status = msg_response['conversation_status']['status']
                        for msg in msg_response['messages']:
                            if msg['message_date']['read'] is not None and msg["to"]["user_id"] == my_id:
                                messages_count += 1
                    except ApiException as e:
                        print('Exception in messages')

                    s = {
                        'pack_id': pack_id,
                        'order_id': order_id,
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
                        'conversation_id': order_id if pack_id == "None" else pack_id,
                        'messages_count': messages_count,
                        'invoice': invoice
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
                        for file in factura_response['fiscal_documents']:
                            if file['file_type'] == 'application/pdf':
                                s['factura'] = file['filename'][:-4].upper()
                                s['factura_id'] = file['id']

                    except ApiException as e:
                        pass

                    resource = 'items/' + str(s['product']['id'])
                    try:
                        response = api_instance.resource_get(resource, access_token)
                        s['product']['image'] = response['thumbnail']
                        s['product']['permalink'] = response['permalink']
                    except ApiException as e:
                        print("Exception in product info")

                    sales.append(s)

            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)

        sales.sort(key=lambda item: item['date'], reverse=True)
        context['sales'] = sales
        return context


class SaleChatView(TemplateView):
    template_name = 'sales/modal_chat.html'

    def get_context_data(self, **kwargs):
        context = super(SaleChatView, self).get_context_data(**kwargs)

        sale_id = self.kwargs['s_pk']
        context['answers'] = Answer.objects.filter(context='c')
        my_id = UserConfig.objects.get(key='meli_user_id').value
        context['my_id'] = int(my_id)
        messages = []

        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            resource = 'messages/packs/' + str(sale_id) + '/sellers/' + my_id + '?tag=post_sale&mark_as_read=false'
            try:
                # Resource path GET
                api_response = api_instance.resource_get(resource, access_token)
                msgs = api_response['messages']
                msgs.sort(key=lambda item: item['message_date']['created'], reverse=True)
                for msg in msgs:
                    m = {
                        'id': msg['id'],
                        'from': msg['from']['user_id'],
                        'text': msg['text'],
                        'date': msg['message_date']['created'],
                    }
                    if msg['message_attachments']:
                        m['attachment'] = {'file': msg['message_attachments'][0]['filename'],
                                           'type': msg['message_attachments'][0]['type']}
                    messages.append(m)

                context['messages'] = messages
                context['sale_id'] = sale_id
                context['buyer_name'] = self.kwargs['buyer']
                context['buyer_id'] = self.kwargs['buyer_id']
            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)

        return context


def get_msg_attachment(request, id):
    with ApiClient() as api_client:
        api_instance = RestClientApi(api_client)
        access_token = UserConfig.objects.get(key='access_token').value
        try:
            attachment_resource = 'messages/attachments/' + id + '?tag=post_sale'
            attachment_response = api_instance.resource_get_file(attachment_resource, access_token)
            with open(attachment_response[0], 'rb') as file:
                response = HttpResponse(file.read(),
                                        content_type=attachment_response[2].get('Content-Type').split()[0])
                response['Content-Disposition'] = 'inline;filename=' + attachment_response[2]['x-original-filename']
            return response
        except ApiException as e:
            print("Exception in attachment info: \n" + e)


def send_message(request):
    response_data = {}
    if request.POST.get('action') == 'post':
        buyer_id = request.POST.get('buyer_id')
        pack_id = request.POST.get('pack_id')
        message = request.POST.get('message')

        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            my_id = UserConfig.objects.get(key='meli_user_id').value
            resource = 'messages/packs/' + str(pack_id) + '/sellers/' + str(my_id) + '?tag=post_sale'
            body = {
                "from": {
                    "user_id": str(my_id),
                },
                "to": {
                    "user_id": str(buyer_id),
                },
                "text": message,
            }

            try:
                # Resource path GET
                api_response = api_instance.resource_post_with_http_info(resource, access_token, body)
                response_data['response'] = api_response[1]
            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)

        response_data['pack_id'] = pack_id
        response_data['message'] = message
        now = datetime.now()
        response_data['time'] = now.strftime("%d de %b - %H:%M")

        return JsonResponse(response_data)


def mark_as_read(request):
    response_data = {}
    if request.POST.get('action') == 'post':
        s_id = request.POST.get('s_id')
        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            my_id = UserConfig.objects.get(key='meli_user_id').value
            access_token = UserConfig.objects.get(key='access_token').value
            resource = 'messages/packs/' + str(s_id) + '/sellers/' + my_id + '?tag=post_sale&mark_as_read=true'
            try:
                # Resource path GET
                api_response = api_instance.resource_get_with_http_info(resource, access_token)
                if api_response[1] == 200:
                    response_data = {'status': 200,
                                     'message': str(_("Marked as read")),
                                     'url': str(reverse_lazy('Sale:list', kwargs={'query': 'new_messages'}))}
                else:
                    response_data = {'status': 300,
                                     'message': str(_("Something went wrong")),
                                     'url': str(reverse_lazy('Sale:list', kwargs={'query': 'new_messages'}))}
            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)

        return HttpResponse(json.dumps(response_data), content_type='application/json')

