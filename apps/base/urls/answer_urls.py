# Django Library
from django.urls import path

# Localfolder Library
from apps.base.views.answer_views import AnswerListView, AnswerDetailView, AnswerCreateView, AnswerUpdateView, \
    AnswerDeleteView, AnswersTable, predefined_answer

app_name = 'Answer'

urlpatterns = [
    path('', AnswerListView.as_view(), name='list'),
    path('<int:pk>', AnswerDetailView.as_view(), name='detail'),
    path('create/', AnswerCreateView.as_view(), name='add'),
    path('update/<int:pk>', AnswerUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', AnswerDeleteView.as_view(), name='delete'),
    path('list_table/', AnswersTable.as_view(), name='answers_list_table'),

    path('predefined', predefined_answer, name='predefined_answer'),
]
