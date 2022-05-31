# Django Library

# Thirdparty Library
from datetime import datetime

from django.http import JsonResponse
from django.views.generic import TemplateView

from apps.base.models import Answer, Invoice
from apps.base.models.customuser_config import UserConfig
from apps.base.views.auth_view import check_meli_session
from apps.meli import ApiException, RestClientApi, ApiClient
from factura_sh.settings import MELI_CLIENT_ID


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
                    resource = 'messages/unread?tag=post_sale&role=seller'
                    api_response = api_instance.resource_get(resource, access_token)
                    for sale in api_response['results']:
                        if sale['resource'].split('/')[4] == UserConfig.objects.get(key="meli_user_id").value:
                            pack_id = sale['resource'].split('/')[2]
                            meli_sales.append(str(pack_id))
                elif query == 'all':
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
                        msg_resource = 'messages/packs/' + str(pack_id) + '/sellers/' + my_id + '?mark_as_read=false'
                        msg_response = api_instance.resource_get(msg_resource, access_token)

                        conversation_status = msg_response['conversation_status']['status']
                        for msg in msg_response['messages']:
                            if msg['message_date']['read'] is not None and msg["to"]["user_id"] == my_id:
                                messages_count += 1
                    except ApiException as e:
                        print('Exception in messages')

                    s = {
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
        context['answers'] = Answer.objects.all()
        my_id = UserConfig.objects.get(key='meli_user_id').value
        context['my_id'] = int(my_id)

        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            resource = 'messages/packs/' + str(sale_id) + '/sellers/' + my_id + '?mark_as_read=false'
            try:
                # Resource path GET
                api_response = api_instance.resource_get(resource, access_token)
                messages = api_response['messages']
                # messages.reverse()
                messages.sort(key=lambda item: item['message_date']['created'], reverse=True)
                context['messages'] = messages
                context['sale_id'] = sale_id
                context['buyer_name'] = self.kwargs['buyer']
                context['buyer_id'] = self.kwargs['buyer_id']
            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)

        return context


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
            resource = 'messages/packs/' + str(pack_id) + '/sellers/' + str(
                my_id) + '?application_id=' + MELI_CLIENT_ID
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


def predefined_answer(request):
    response_data = {}
    if request.POST.get('action') == 'get':
        key = request.POST.get('key')
        message = Answer.objects.get(name=key).message
        response_data['message'] = message
        return JsonResponse(response_data)

    if request.POST.get('action') == 'post':
        key = request.POST.get('key')
        message = request.POST.get('message')
        m, created = Answer.objects.get_or_create(
            name=key,
            message=message
        )
        if created:
            response_data['message'] = message
            return JsonResponse(response_data)
        else:
            response_data['message'] = m.message
            return JsonResponse(response_data)