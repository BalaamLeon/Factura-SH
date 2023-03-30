# Django Library
from django.urls import path

# Localfolder Library
from apps.base.views.melipost_view import MeliPostListView, MeliPostDetailView, MeliPostCreateView, MeliPostUpdateView, \
    MeliPostDeleteView, MeliPostsTable, predefined_melipost

app_name = 'MeliPost'

urlpatterns = [
    path('', MeliPostListView.as_view(), name='list'),
    path('<int:pk>', MeliPostDetailView.as_view(), name='detail'),
    path('create/', MeliPostCreateView.as_view(), name='add'),
    path('update/<int:pk>', MeliPostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', MeliPostDeleteView.as_view(), name='delete'),
    path('list_table/', MeliPostsTable.as_view(), name='meliposts_list_table'),

    path('predefined', predefined_melipost, name='predefined_melipost'),
]
