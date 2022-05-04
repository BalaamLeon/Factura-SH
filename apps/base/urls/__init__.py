"""uRLs para base
"""
# Django Library
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('app/', include('apps.base.urls.base')),
    path('', include('apps.base.urls.customuser_urls')),
    path('customer/', include('apps.base.urls.customer_urls')),
    path('invoice/', include('apps.base.urls.invoice_urls')),
    path('', include('apps.base.urls.front_urls')),
]
