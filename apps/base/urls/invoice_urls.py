# Django Library
from django.urls import path

# Localfolder Library
from apps.base.views.invoice_views import InvoiceListView, InvoiceDetailView, InvoiceCreateView, \
    InvoiceDeleteView, invoice_get_id, get_invoice_name, invoices, \
    invoice_invoice_list, invoice_invoices, InvoicesTable, SendCFDI, get_cfdi, set_tracking, change_status, \
    InvoiceFromSaleCreateView

app_name = 'Invoice'

urlpatterns = [
    path('<str:query>', InvoiceListView.as_view(), name='list'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='detail'),
    path('create/', InvoiceCreateView.as_view(), name='add'),
    path('create/<str:id>', InvoiceFromSaleCreateView.as_view(), name='add_from_sale'),
    # path('update/<int:pk>/', InvoiceUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', InvoiceDeleteView.as_view(), name='delete'),
    path('get_id', invoice_get_id, name='invoice_get_id'),
    path('get_name', get_invoice_name, name='get_invoice_name'),
    path('list_table/<str:query>', InvoicesTable.as_view(), name='invoices_list_table'),
    path('all_data', invoices, name='invoices'),
    path('send_cfdi/<int:id>/', SendCFDI.as_view(), name='send_cfdi'),
    path('get_cfdi/<int:pack_id>/<str:file_id>', get_cfdi, name='get_cfdi'),
    path('set_tracking/<int:id>', set_tracking, name='set_tracking'),
    path('change_status/<int:pk>', change_status.as_view(), name='change_status'),

    path('<int:s_pk>/invoices', invoice_invoice_list, name='invoice_invoice_list'),
    path('<int:s_pk>/all/', invoice_invoices, name='invoice_invoices'),

]
