# Django Library
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Localfolder Library
from apps.base.forms.answer_form import AnswerForm
from apps.base.models import Answer
from apps.base.views.father_view import FatherListView, FatherDetailView, FatherCreateView, FatherUpdateView, \
    FatherTableListView, FatherDeleteView


OBJECT_FIELDS = [
    {'string': _("Name"), 'field': 'name'},
    {'string': _("Message"), 'field': 'message'},
    {'string': _("Context"), 'field': 'get_context_display'},
]

OBJECT_LIST_FIELDS = [
    {'string': _("Name"), 'field': 'name'},
    {'string': _("Message"), 'field': 'message'},
    {'string': _("Context"), 'field': 'get_context_display'},
]

OBJECT_FORM_FIELDS = [
    'name',
    'message',
    'context',
]


# ========================================================================== #
class AnswerListView(FatherListView):
    model = Answer
    template_name = 'common/list.html'
    extra_context = {'fields': OBJECT_LIST_FIELDS,
                     'modal_add': True,
                     }


# ========================================================================== #
class AnswerDetailView(FatherDetailView):
    model = Answer
    template_name = 'common/detail.html'
    extra_context = {'fields': OBJECT_LIST_FIELDS}


# ========================================================================== #
class AnswerCreateView(BSModalCreateView, FatherCreateView):
    model = Answer
    # fields = OBJECT_FORM_FIELDS
    form_class = AnswerForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: Answer was created.'
    success_url = reverse_lazy('Answer:list')


# ========================================================================== #
class AnswerDeleteView(BSModalDeleteView, FatherDeleteView):
    model = Answer


# ========================================================================== #
class AnswerUpdateView(BSModalUpdateView, FatherUpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'common/modal_form.html'
    success_message = 'Success: Answer was updated.'
    success_url = reverse_lazy('Answer:list')


# ========================================================================== #
class AnswersTable(FatherTableListView):
    model = Answer
    fields = OBJECT_LIST_FIELDS



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
        m.context = request.POST.get('context')
        m.save()
        if created:
            response_data['message'] = message
            return JsonResponse(response_data)
        else:
            response_data['message'] = m.message
            return JsonResponse(response_data)
