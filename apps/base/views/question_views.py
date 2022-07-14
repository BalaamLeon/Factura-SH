# Django Library
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

# Thirdparty Library
from datetime import datetime
import timeago as timeago

# Localfolder Library
from apps.base.models import Answer
from apps.base.models.customuser_config import UserConfig
from apps.base.views.auth_view import check_meli_session
from apps.meli import ApiException, RestClientApi, ApiClient


# ========================================================================== #
class QuestionListView(TemplateView):
    template_name = 'question/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # query = self.kwargs['query']
        questions = {}

        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            my_id = UserConfig.objects.get(key='meli_user_id').value

            try:
                context['page_title'] = _('Mercado Libre Questions')
                # questions_resource = 'questions/search?seller_id=' + my_id + '&sort_fields=date_created&sort_types=DESC'
                questions_resource = 'questions/search?seller_id=' + my_id + '&status=UNANSWERED&sort_fields=date_created&sort_types=DESC'
                questions_response = api_instance.resource_get(questions_resource, access_token)

                for question in questions_response['questions']:
                    if question['item_id'] not in questions:
                        item_resource = 'items/' + question['item_id']
                        item_response = api_instance.resource_get(item_resource, access_token)
                        item = {'thumbnail': item_response['thumbnail'],
                                'title': item_response['title'],
                                'price': item_response['price'],
                                'stock': item_response['available_quantity'],
                                'url': item_response['permalink'],
                                'catalog': item_response['catalog_listing'],
                                'shipping': '',
                                'status': '',
                                }

                        if item_response['shipping']['free_shipping']:
                            item['shipping'] = _('Free Shipping')

                        if item_response['status'] == 'paused' and len(item_response['sub_status']) > 0:
                            if item_response['sub_status'][0] == 'out_of_stock':
                                item['status'] = _('Paused out of stock')

                        for att in item_response['attributes']:
                            if att['id'] == 'SELLER_SKU':
                                item['sku'] = att['value_name']
                                break

                        questions[question['item_id']] = item
                        questions[question['item_id']]['questions'] = []

                    customer_resource = 'users/' + str(question['from']['id'])
                    customer_response = api_instance.resource_get(customer_resource, access_token)
                    question['customer'] = customer_response['nickname']

                    question_date = datetime.strptime(question['date_created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                    question_date = question_date.replace(tzinfo=None)
                    now = datetime.now()
                    question_date_ago = timeago.format(question_date, now, 'es')
                    question['date'] = question_date_ago

                    questions[question['item_id']]['questions'].append(question)

            #         try:
            #             invoice = Invoice.objects.get(meli_id=pack_id)
            #         except Invoice.DoesNotExist:
            #             invoice = None
            #         resource = 'packs/' + pack_id
            #         response = None
            #         messages_count = 0
            #         conversation_status = 'blocked'
            #
            #         try:
            #             response = api_instance.resource_get(resource, access_token)
            #             order_id = str(response['orders'][0]['id'])
            #             resource = 'orders/' + order_id
            #             response = api_instance.resource_get(resource, access_token)
            #         except ApiException as e:
            #             print('Exception in pack info')
            #             try:
            #                 order_id = pack_id
            #                 resource = 'orders/' + order_id
            #                 response = api_instance.resource_get(resource, access_token)
            #                 pack_id = str(response['pack_id'])
            #
            #             except ApiException as e:
            #                 print('Exception in order info')
            #
            #         try:
            #             msg_resource = 'messages/packs/' + str(pack_id) + '/sellers/' \
            #                            + my_id + '?tag=post_question&mark_as_read=false'
            #             msg_response = api_instance.resource_get(msg_resource, access_token)
            #
            #             conversation_status = msg_response['conversation_status']['status']
            #             for msg in msg_response['messages']:
            #                 if msg['message_date']['read'] is not None and msg["to"]["user_id"] == my_id:
            #                     messages_count += 1
            #         except ApiException as e:
            #             print('Exception in messages')
            #
            #         s = {
            #             'pack_id': pack_id,
            #             'order_id': order_id,
            #             'channel': response['context']['channel'],
            #             'id': response['id'],
            #             'date': datetime.fromisoformat(response['date_created']),
            #             'buyer_id': response['buyer']['id'],
            #             'buyer_name': response['buyer']['first_name'] + ' ' + response['buyer']['last_name'],
            #             'buyer_nickname': response['buyer']['nickname'],
            #             'products': response['order_items'],
            #             'product': {'image': None,
            #                         'id': response['order_items'][0]['item']['id'],
            #                         'title': response['order_items'][0]['item']['title'],
            #                         'unit_price': response['order_items'][0]['unit_price'],
            #                         'quantity': response['order_items'][0]['quantity'],
            #                         'seller_sku': response['order_items'][0]['item']['seller_sku'],
            #                         },
            #             'conversation_status': conversation_status,
            #             'messages_count': messages_count,
            #             'invoice': invoice
            #         }
            #
            #         resource = 'shipments/' + str(response['shipping']['id'])
            #         try:
            #             response = api_instance.resource_get(resource, access_token)
            #             s['shipping_status'] = response['status']
            #             s["logistic_type"] = response["logistic_type"]
            #             if response['status'] == 'delivered':
            #                 s['date_delivered'] = datetime.fromisoformat(response['status_history']['date_delivered'])
            #             elif response['status'] == 'ready_to_ship' or response['status'] == 'shipped':
            #                 s['date_delivered'] = datetime.fromisoformat(
            #                     response['shipping_option']['estimated_delivery_final']['date'])
            #
            #         except ApiException as e:
            #             print("Exception in shipping info")
            #
            #         factura_resource = 'packs/' + str(pack_id) + '/fiscal_documents'
            #         try:
            #             factura_response = api_instance.resource_get(factura_resource, access_token)
            #             for file in factura_response['fiscal_documents']:
            #                 if file['file_type'] == 'application/pdf':
            #                     s['factura'] = file['filename'][:-4].upper()
            #                     s['factura_id'] = file['id']
            #
            #         except ApiException as e:
            #             pass
            #
            #         resource = 'items/' + str(s['product']['id'])
            #         try:
            #             response = api_instance.resource_get(resource, access_token)
            #             s['product']['image'] = response['thumbnail']
            #             s['product']['permalink'] = response['permalink']
            #         except ApiException as e:
            #             print("Exception in product info")
            #
            #         questions.append(s)
            #
            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)

        context['questions'] = questions

        context['answers'] = Answer.objects.filter(context='q')
        context['js_files'] = ['dist/js/questions.js']
        return context


def send_answer(request):
    response_data = {}
    if request.POST.get('action') == 'post':
        question_id = request.POST.get('question_id')
        message = request.POST.get('message')
        print(question_id, message)

        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            resource = 'answers'
            body = {
                "question_id": question_id,
                "text": message,
            }

            try:
                # Resource path GET
                api_response = api_instance.resource_post(resource, access_token, body)
                response_data['response'] = api_response[1]
            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)
                response_data['response'] = e.body

        return JsonResponse(response_data)
