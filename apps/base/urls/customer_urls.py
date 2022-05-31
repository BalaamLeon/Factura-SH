# Django Library
from django.urls import path

# Localfolder Library
from apps.base.views.customer_views import CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView, \
    CustomerDeleteView, customer_get_id, get_customer_name, customers, \
    customer_invoice_list, customer_invoices, CustomersTable, get_customer_info

app_name = 'Customer'

urlpatterns = [
    path('', CustomerListView.as_view(), name='list'),
    path('<int:pk>', CustomerDetailView.as_view(), name='detail'),
    path('create/', CustomerCreateView.as_view(), name='add'),
    path('update/<int:pk>', CustomerUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CustomerDeleteView.as_view(), name='delete'),
    path('get_id', customer_get_id, name='customer_get_id'),
    path('get_name', get_customer_name, name='get_customer_name'),
    path('get_info', get_customer_info, name='get_info'),
    path('list_table/', CustomersTable.as_view(), name='customers_list_table'),
    path('all_data', customers, name='customers'),

    path('<int:s_pk>/invoices', customer_invoice_list, name='customer_invoice_list'),
    path('<int:s_pk>/all/', customer_invoices, name='customer_invoices'),

]
