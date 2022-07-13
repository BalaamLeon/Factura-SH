# Django Library
from django.urls import path

# Localfolder Library
from apps.base.views.question_views import QuestionListView, send_answer

app_name = 'Question'

urlpatterns = [
    path('', QuestionListView.as_view(), name='list'),
    path('answer', send_answer, name='send_answer'),
]
