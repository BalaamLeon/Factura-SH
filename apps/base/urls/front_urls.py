# Django Library
from django.urls import path

# Localfolder Library
from apps.base.views.factura_views import FacturaDetailView, FacturaCustomerCreateView, FacturaCustomerUpdateView, \
    FacturaCustomerDeleteView, search_rfc, search_rfc_view, SearchView, FacturaInvoiceCreateView, \
    FacturaInvoiceSuccessView

app_name = 'Factura'

urlpatterns = [
    path('', SearchView.as_view(), name='list'),
    path('<int:pk>', FacturaDetailView.as_view(), name='detail'),
    path('create/<str:rfc>/', FacturaCustomerCreateView.as_view(), name='add'),
    path('update/<int:pk>/', FacturaCustomerUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', FacturaCustomerDeleteView.as_view(), name='delete'),
    path('search/', search_rfc_view, name='search'),

    path('invoice/<int:pk>/', FacturaInvoiceCreateView.as_view(), name='invoice'),
    path('success/', FacturaInvoiceSuccessView.as_view(), name='success'),
    # path('search_rfc/', search_rfc, name='search_rfc'),
]
