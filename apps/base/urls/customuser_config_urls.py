"""The store routes
"""
# Django Library
from django.urls import path

# Localfolder Library
from apps.base.views.customuser_config import ParameterListView, ParameterCreateView, ParameterDetailView, \
    ParameterUpdateView, ParameterDeleteView

app_name = 'UserConfig'

urlpatterns = [
    path('', ParameterListView.as_view(), name='list'),
    path('add/', ParameterCreateView.as_view(), name='add'),
    path('<int:pk>/', ParameterDetailView.as_view(), name='detail'),
    path('<int:pk>/update', ParameterUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ParameterDeleteView.as_view(), name='delete'),
]
