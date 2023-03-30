# Django Library
from django.urls import path

# Localfolder Library
from apps.base.views.quzpide_views import QuzpideSaleListView, QuzpideSaleChatView, QuzpideDesignCreateView, \
    QuzpideDesignSuccessView, CreateImageView
from apps.base.views.sale_views import SaleListView, SaleChatView, send_message, get_msg_attachment, \
    mark_as_read

app_name = 'Quzpide'

urlpatterns = [
    path('sales/<str:query>/', QuzpideSaleListView.as_view(), name='list'),
    path('<int:s_pk>/<str:buyer>/<int:buyer_id>/chat', QuzpideSaleChatView.as_view(), name='chat'),
    path('send_message', send_message, name='send_message'),
    path('mark_as_read', mark_as_read, name='mark_as_read'),
    path('attachment/<str:id>', get_msg_attachment, name='attachment'),

    path('<int:meli_sale>/', QuzpideDesignCreateView.as_view(), name='invoice'),
    path('image/create', CreateImageView, name="image_create"),
    path('success/', QuzpideDesignSuccessView.as_view(), name='success'),
]
