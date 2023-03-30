# Django Library
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Localfolder Library
from apps.base.forms.melipost_form import MeliPostForm
from apps.base.models import UserConfig
from apps.base.models.meli_post import MeliPost
from apps.base.views.auth_view import check_meli_session
from apps.base.views.father_view import FatherListView, FatherDetailView, FatherCreateView, FatherUpdateView, \
    FatherTableListView, FatherDeleteView
from apps.meli import ApiClient, RestClientApi, ApiException

OBJECT_FIELDS = [
    {'string': _("ID"), 'field': 'meli_id'},
    {'string': _("Title"), 'field': 'title'},
]

OBJECT_LIST_FIELDS = [
    {'string': _("ID"), 'field': 'meli_id'},
    {'string': _("Title"), 'field': 'title'},
]

OBJECT_FORM_FIELDS = [
    'meli_id',
    'title',
]


# ========================================================================== #
class MeliPostListView(FatherListView):
    model = MeliPost
    template_name = 'common/list.html'
    extra_context = {'fields': OBJECT_LIST_FIELDS,
                     'modal_add': True,
                     }


# ========================================================================== #
class MeliPostDetailView(FatherDetailView):
    model = MeliPost
    template_name = 'common/detail.html'
    extra_context = {'fields': OBJECT_LIST_FIELDS}


# ========================================================================== #
class MeliPostCreateView(BSModalCreateView, FatherCreateView):
    model = MeliPost
    # fields = OBJECT_FORM_FIELDS
    form_class = MeliPostForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: MeliPost was created.'
    success_url = reverse_lazy('MeliPost:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        check_meli_session()
        with ApiClient() as api_client:
            api_instance = RestClientApi(api_client)
            access_token = UserConfig.objects.get(key='access_token').value
            my_id = UserConfig.objects.get(key='meli_user_id').value
            try:
                resource = 'items/' + self.object.meli_id
                api_response = api_instance.resource_get(resource, access_token)

                self.object.title = api_response['title']
                self.object.save()
                return super(MeliPostCreateView, self).form_valid(form)
            except ApiException as e:
                print("Exception when calling OAuth20Api->get_token: %s\n" % e)


# ========================================================================== #
class MeliPostDeleteView(BSModalDeleteView, FatherDeleteView):
    model = MeliPost


# ========================================================================== #
class MeliPostUpdateView(BSModalUpdateView, FatherUpdateView):
    model = MeliPost
    form_class = MeliPostForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: MeliPost was updated.'
    success_url = reverse_lazy('MeliPost:list')


# ========================================================================== #
class MeliPostsTable(FatherTableListView):
    model = MeliPost
    fields = OBJECT_LIST_FIELDS


def predefined_melipost(request):
    response_data = {}
    if request.POST.get('action') == 'get':
        key = request.POST.get('key')
        message = MeliPost.objects.get(name=key).message
        response_data['message'] = message
        return JsonResponse(response_data)

    if request.POST.get('action') == 'post':
        key = request.POST.get('key')
        message = request.POST.get('message')
        m, created = MeliPost.objects.get_or_create(
            name=key,
            message=message
        )
        m.context = request.POST.get('context')
        m.save()
        if created:
            response_data['message'] = message
            return JsonResponse(response_data)
        else:
            response_data['message'] = m.message
            return JsonResponse(response_data)
