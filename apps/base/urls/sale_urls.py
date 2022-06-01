# Django Library
from django.urls import path

# Localfolder Library
from apps.base.views.sale_views import SaleListView, SaleChatView, send_message, predefined_answer, get_msg_attachment

app_name = 'Sale'

urlpatterns = [
    path('<str:query>/', SaleListView.as_view(), name='list'),
    path('<int:s_pk>/<str:buyer>/<int:buyer_id>/chat', SaleChatView.as_view(), name='chat'),
    path('send_message', send_message, name='send_message'),
    path('attachment/<str:id>', get_msg_attachment, name='attachment'),
    path('predefined_answer', predefined_answer, name='predefined_answer'),
]
