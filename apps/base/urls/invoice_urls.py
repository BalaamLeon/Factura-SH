# Django Library
from django.urls import path

# Localfolder Library
from apps.base.views.invoice_views import InvoiceListView, InvoiceDetailView, InvoiceCreateView, InvoiceUpdateView, \
    InvoiceDeleteView, invoice_get_id, get_invoice_name, invoices, \
    invoice_invoice_list, invoice_invoices, InvoicesTable

app_name = 'Invoice'

urlpatterns = [
    path('', InvoiceListView.as_view(), name='list'),
    path('<int:pk>', InvoiceDetailView.as_view(), name='detail'),
    path('create/', InvoiceCreateView.as_view(), name='add'),
    path('update/<int:pk>', InvoiceUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', InvoiceDeleteView.as_view(), name='delete'),
    path('get_id', invoice_get_id, name='invoice_get_id'),
    path('get_name', get_invoice_name, name='get_invoice_name'),
    path('list_table/', InvoicesTable.as_view(), name='invoices_list_table'),
    path('all_data', invoices, name='invoices'),

    path('<int:s_pk>/invoices', invoice_invoice_list, name='invoice_invoice_list'),
    path('<int:s_pk>/all/', invoice_invoices, name='invoice_invoices'),

]
